import logging
import typing
import urllib.parse
from hashlib import md5

import aiohttp

from aiovkapi.exception import APIError, ErrorHandler
from aiovkapi.session import AiohttpSession, BaseSession
from aiovkapi.token_generator import TokenGenerator, Token

__all__ = (
    'API',
)

from aiovkapi.types.all_methods import APICategories

logger = logging.getLogger('aiovkapi')
LANG_TYPING = typing.Literal[
    # русский
    'ru', 0,
    # украинский
    'uk', 1,
    # белорусский
    'be', 2,
    # английский
    'en', 3,
    # испанский
    'es', 4,
    # финский
    'fi', 5,
    # немецкий
    'de', 6,
    # итальянский
    'it', 7
]


class API(APICategories):
    error_handlers: typing.List[ErrorHandler]

    def __init__(
            self,
            tokens: typing.Union[typing.List[typing.Union[str, Token, dict]], TokenGenerator],
            version: str = '5.131',
            lang: str = LANG_TYPING,
            session: BaseSession = AiohttpSession(),
            base_url: str = 'https://api.vk.com/method',
            test_mode: typing.Union[typing.Literal[1], typing.Literal[0]] = 0,
            **extra
    ):
        if isinstance(tokens, TokenGenerator):
            self._tokens = tokens
        elif isinstance(tokens, list):
            _tokens = []
            for token in tokens:
                if isinstance(token, Token):
                    _tokens.append(token)
                elif isinstance(token, str):
                    _tokens.append(Token(access_token=token))
                elif isinstance(token, dict):
                    _tokens.append(Token(**token))
                else:
                    raise ValueError("Invalid tokens type")
            self._tokens = TokenGenerator(*_tokens)
        else:
            raise ValueError("Invalid tokens type")
        self.version = version
        self.lang = lang
        self.session = session
        self.base_url = base_url
        self.extra = extra
        self.error_handlers = []
        self.test_mode = test_mode
        APICategories.__init__(self, self)

    @staticmethod
    def calc_sig(
            token: Token,
            method: str,
            req_params: dict
    ) -> str:
        """Генерирует подпись запроса

        Параметр sig равен md5 от конкатенации следующих строк:

        - Строки **/method/{method}?**
        - Пар **"parameter_name=parameter_value"**, расположенных в порядке возрастания имени параметра.
        - Защищенного секрета приложения **api_secret**.

        `sig = md5(/method/{method}?name1=value1&name2=value2api_secret)`

        :param token: Токен
        :param method: Вызванный метод
        :param req_params: Параметры запроса
        :return: Подпись
        """
        if not token.client_secret:
            raise ValueError(f"client_secret fot token {token!r} required")
        to_hash = urllib.parse.urlencode(req_params) + token.client_secret
        to_hash = f"/method/{method}?" + to_hash
        return md5(to_hash.encode()).hexdigest()

    async def method(
            self,
            method: str,
            dataclass: typing.Any = dict,
            no_error: bool = False,
            raw: bool = False,
            **values
    ) -> typing.Any:
        token = self._tokens.get_token()

        req_params = {
            key: value
            for key, value in sorted(
                {
                    "v": self.version,
                    "https": 1,
                    "lang": self.lang,
                    "access_token": token.access_token,
                    "test_mode": self.test_mode
                }.items(),
                key=lambda x: x[0]
            )
        }
        if not self.test_mode:
            req_params.pop("test_mode")
        if token.client_id is not None and token.client_secret is not None:
            req_params['sig'] = self.calc_sig(
                token,
                method,
                req_params
            )
        url = f"{self.base_url}/{method}?" + urllib.parse.urlencode(req_params)

        form = aiohttp.FormData()
        for key, value in values.items():
            if hasattr(value, 'to_vk_api'):
                form.add_field(key, await value.to_vk_api(self))
            else:
                form.add_field(key, value)
        logger.debug(f"Make request to {method} with data {values!r}")
        raw_response = await self.session.post(url, form, headers={'User-Agent': token.user_agent})
        logger.debug(f"Response is {raw_response!r}")
        if 'error' in raw_response:
            if no_error:
                return None
            exception = APIError(
                raw_response['error'],
                self,
                method,
                dataclass,
                no_error,
                values
            )
            for error_handler in self.error_handlers:
                if error_handler.code == exception.status_code:
                    return await error_handler.handle(self, exception, self.extra)
            raise exception
        if raw:
            return raw_response
        response = raw_response['response']
        if isinstance(response, list):
            new_list = []
            for item in response:
                if isinstance(item, dict):
                    new_list.append(dataclass(**item))
                else:
                    new_list.append(item)
            return new_list
        elif isinstance(response, dict):
            return dataclass(**response)
        return response

    async def close(self):
        await self.session.close()
