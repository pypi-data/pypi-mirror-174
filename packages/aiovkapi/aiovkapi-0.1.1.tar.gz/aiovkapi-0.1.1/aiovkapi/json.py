import abc
import json
import typing

__all__ = (
    'BaseJson',
    'Json',
    'OrJson',
    'get_json_module'
)

cached_module: typing.Optional["BaseJson"] = None


class BaseJson(abc.ABC):

    def dumps(self, data: dict) -> str:
        ...

    def loads(self, data: typing.Union[str, bytes]) -> dict:
        ...


class Json(BaseJson):

    def __init__(self, dumps_kw: dict = None, loads_kw: dict = None):
        self.dumps_kw = dumps_kw or {}
        self.loads_kw = loads_kw or {}

    def dumps(self, data: dict) -> str:
        return json.dumps(data, **self.dumps_kw)

    def loads(self, data: typing.Union[str, bytes]) -> dict:
        return json.loads(data, **self.loads_kw)


class OrJson(BaseJson):

    def __init__(self, dumps_kw: dict = None, loads_kw: dict = None):
        self.dumps_kw = dumps_kw or {}
        self.loads_kw = loads_kw or {}

    def dumps(self, data: dict) -> str:
        try:
            import orjson
            return orjson.dumps(data, **self.dumps_kw).decode('utf-8')
        except ImportError as ex:
            raise RuntimeError("Install orjson pls") from ex

    def loads(self, data: typing.Union[str, bytes]) -> dict:
        try:
            import orjson
            return json.loads(data, **self.loads_kw)
        except ImportError as ex:
            raise RuntimeError("Install orjson pls") from ex


def get_json_module() -> BaseJson:
    global cached_module
    if not cached_module:
        try:
            import orjson
            cached_module = OrJson()
        except ImportError:
            cached_module = Json()
    return cached_module