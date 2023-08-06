import abc
import typing

import aiohttp

from aiovkapi.json import BaseJson, get_json_module

__all__ = (
    'BaseSession',
    'AiohttpSession',
)


class BaseSession(abc.ABC):

    @abc.abstractmethod
    async def close(self):
        ...

    @abc.abstractmethod
    async def get(self, url: str, **extra) -> dict:
        ...

    @abc.abstractmethod
    async def post(self, url: str, data: typing.Any, **extra) -> dict:
        ...


class AiohttpSession(BaseSession):
    _session: typing.Optional[aiohttp.ClientSession]
    _json: BaseJson

    def __init__(
            self,
            json: BaseJson = get_json_module(),
            client_kwargs: dict = None
    ):
        self._json = json
        self._session = None
        self._client_kwargs = client_kwargs or {}

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            self._session = aiohttp.ClientSession(**self._client_kwargs)
        return self._session

    async def close(self):
        if not self._session:
            return
        if self._session.closed:
            return
        await self._session.close()

    async def get(self, url: str, **extra) -> dict:
        async with self.session.get(url, **extra) as response:
            return self._json.loads(await response.read())

    async def post(self, url: str, data: typing.Any, **extra) -> dict:
        async with self.session.post(url, data=data, **extra) as response:
            return self._json.loads(await response.read())
