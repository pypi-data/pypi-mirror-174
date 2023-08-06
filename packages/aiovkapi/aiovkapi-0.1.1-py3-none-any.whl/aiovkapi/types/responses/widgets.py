import typing

from aiovkapi.types.objects import WidgetsWidgetComment, WidgetsWidgetPage
from aiovkapi.types.responses.base_response import BaseResponse


class GetCommentsResponse(BaseResponse):
    response: "GetCommentsResponseModel"


class GetPagesResponse(BaseResponse):
    response: "GetPagesResponseModel"


class GetCommentsResponseModel(BaseResponse):
    count: typing.Optional[int] = None
    posts: typing.Optional[typing.List["WidgetsWidgetComment"]] = None


class GetPagesResponseModel(BaseResponse):
    count: typing.Optional[int] = None
    pages: typing.Optional[typing.List["WidgetsWidgetPage"]] = None


__all__ = (
    "GetCommentsResponse",
    "GetCommentsResponseModel",
    "GetPagesResponse",
    "GetPagesResponseModel",
    "WidgetsWidgetComment",
    "WidgetsWidgetPage",
)
