import typing

from aiovkapi.types.methods.base_category import BaseCategory
from aiovkapi.types.responses.base import OkResponse
from aiovkapi.types.responses.streaming import (
    GetServerUrlResponse,
    GetServerUrlResponseModel,
)
from typing_extensions import Literal


class StreamingCategory(BaseCategory):
    async def get_server_url(self, **kwargs) -> GetServerUrlResponseModel:
        """Allows to receive data for the connection to Streaming API."""

        params = self.get_set_params(locals())
        response = await self.request("streaming.getServerUrl", params)
        model = GetServerUrlResponse
        return model(**response).response

    async def set_settings(
        self,
        monthly_tier: typing.Optional[
            Literal[
                "tier_1", "tier_2", "tier_3", "tier_4", "tier_5", "tier_6", "unlimited"
            ]
        ] = None,
        **kwargs
    ) -> int:
        """streaming.setSettings method

        :param monthly_tier:
        """

        params = self.get_set_params(locals())
        response = await self.request("streaming.setSettings", params)
        model = OkResponse
        return model(**response).response


__all__ = ("StreamingCategory",)
