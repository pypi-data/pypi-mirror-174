from aiovkapi.types.objects import StatusStatus
from aiovkapi.types.responses.base_response import BaseResponse


class GetResponse(BaseResponse):
    response: StatusStatus


__all__ = (
    "GetResponse",
    "StatusStatus",
)
