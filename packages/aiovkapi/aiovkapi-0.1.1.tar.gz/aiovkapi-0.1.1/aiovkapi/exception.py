import typing

if typing.TYPE_CHECKING:
    from aiovkapi.api import API

__all__ = (
    'APIError',
    'ErrorHandler',
)


class APIError(Exception):
    description: str
    status_code: int
    extra_fields: dict

    def __init__(
            self,
            error_data: dict,
            api: 'API',
            method: str,
            dataclass: typing.Any = dict,
            no_error: bool = False,
            values: dict = None
    ):
        self.description = error_data.pop('error_msg')
        self.status_code = error_data.pop('error_code')
        self.extra_fields = error_data

        self._api = api
        self._method = method
        self._dataclass = dataclass
        self._no_error = no_error
        self._values = values

    async def retry(self, **data) -> typing.Any:
        return await self._api.method(
            self._method,
            self._dataclass,
            self._no_error,
            **(self._values | data)
        )

    def __str__(self):
        return f"[{self.status_code}] {self.description}"


class ErrorHandler:
    code: int

    def __init__(
            self,
            code: int,
            handler: typing.Callable[['ErrorHandler', 'API', 'APIError', dict], typing.Awaitable]
    ):
        self.code = code
        self._handler = handler
        self.identity = f"{self.code}_{self._handler.__name__}"

    async def handle(self, api: 'API', exception: 'APIError', extra: dict):
        return await self._handler(self, api, exception, extra)


