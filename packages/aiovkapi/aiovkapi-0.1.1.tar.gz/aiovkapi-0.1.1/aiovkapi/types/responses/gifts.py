import typing

from aiovkapi.types.objects import GiftsGift
from aiovkapi.types.responses.base_response import BaseResponse


class GetResponse(BaseResponse):
    response: "GetResponseModel"


class GetResponseModel(BaseResponse):
    count: typing.Optional[int] = None
    items: typing.Optional[typing.List["GiftsGift"]] = None


__all__ = (
    "GetResponse",
    "GetResponseModel",
    "GiftsGift",
)
