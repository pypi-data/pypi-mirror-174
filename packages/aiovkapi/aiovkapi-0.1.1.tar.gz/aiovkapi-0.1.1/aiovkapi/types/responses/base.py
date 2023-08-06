from aiovkapi.types.objects import BaseBoolInt, BaseUploadServer
from aiovkapi.types.responses.base_response import BaseResponse


class BoolResponse(BaseResponse):
    response: BaseBoolInt


class OkResponse(BaseResponse):
    response: int


class BaseGetUploadServerResponse(BaseResponse):
    response: BaseUploadServer


__all__ = (
    "BaseBoolInt",
    "BaseGetUploadServerResponse",
    "BaseUploadServer",
    "BoolResponse",
    "OkResponse",
)
