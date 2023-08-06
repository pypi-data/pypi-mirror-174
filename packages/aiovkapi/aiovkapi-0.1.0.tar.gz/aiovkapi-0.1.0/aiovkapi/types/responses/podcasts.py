import typing

from aiovkapi.types.objects import PodcastExternalData
from aiovkapi.types.responses.base_response import BaseResponse


class SearchPodcastResponse(BaseResponse):
    response: "SearchPodcastResponseModel"


class SearchPodcastResponseModel(BaseResponse):
    podcasts: typing.Optional[typing.List["PodcastExternalData"]] = None
    results_total: typing.Optional[int] = None


__all__ = (
    "PodcastExternalData",
    "SearchPodcastResponse",
    "SearchPodcastResponseModel",
)
