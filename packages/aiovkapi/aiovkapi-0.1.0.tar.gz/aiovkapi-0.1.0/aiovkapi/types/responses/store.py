import typing

from aiovkapi.types.objects import BaseSticker, StoreProduct, StoreStickersKeyword
from aiovkapi.types.responses.base_response import BaseResponse


class GetFavoriteStickersResponse(BaseResponse):
    response: typing.List["BaseSticker"]


class GetProductsResponse(BaseResponse):
    response: typing.List["StoreProduct"]


class GetStickersKeywordsResponse(BaseResponse):
    response: "GetStickersKeywordsResponseModel"


class GetStickersKeywordsResponseModel(BaseResponse):
    count: typing.Optional[int] = None
    dictionary: typing.Optional[typing.List["StoreStickersKeyword"]] = None
    chunks_count: typing.Optional[int] = None
    chunks_hash: typing.Optional[str] = None


__all__ = (
    "BaseSticker",
    "GetFavoriteStickersResponse",
    "GetProductsResponse",
    "GetStickersKeywordsResponse",
    "GetStickersKeywordsResponseModel",
    "StoreProduct",
    "StoreStickersKeyword",
)
