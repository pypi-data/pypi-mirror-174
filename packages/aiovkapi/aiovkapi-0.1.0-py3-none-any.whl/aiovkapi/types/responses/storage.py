import typing

from aiovkapi.types.objects import StorageValue
from aiovkapi.types.responses.base_response import BaseResponse


class GetKeysResponse(BaseResponse):
    response: typing.List[str]


class GetResponse(BaseResponse):
    response: typing.List["StorageValue"]


__all__ = (
    "GetKeysResponse",
    "GetResponse",
    "StorageValue",
)
