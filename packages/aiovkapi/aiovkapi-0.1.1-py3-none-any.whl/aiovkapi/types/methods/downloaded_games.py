import typing

from aiovkapi.types.methods.base_category import BaseCategory
from aiovkapi.types.responses.downloaded_games import (
    PaidStatusResponse,
    PaidStatusResponseModel,
)


class DownloadedGamesCategory(BaseCategory):
    async def get_paid_status(
        self, user_id: typing.Optional[int] = None, **kwargs
    ) -> PaidStatusResponseModel:
        """downloadedGames.getPaidStatus method

        :param user_id:
        """

        params = self.get_set_params(locals())
        response = await self.request("downloadedGames.getPaidStatus", params)
        model = PaidStatusResponse
        return model(**response).response


__all__ = ("DownloadedGamesCategory",)
