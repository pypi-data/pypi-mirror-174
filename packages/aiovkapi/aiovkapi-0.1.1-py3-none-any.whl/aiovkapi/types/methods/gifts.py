import typing

from aiovkapi.types.methods.base_category import BaseCategory
from aiovkapi.types.responses.gifts import GetResponse, GetResponseModel


class GiftsCategory(BaseCategory):
    async def get(
        self,
        user_id: typing.Optional[int] = None,
        count: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        **kwargs
    ) -> GetResponseModel:
        """Returns a list of user gifts.

        :param user_id: User ID.
        :param count: Number of gifts to return.
        :param offset: Offset needed to return a specific subset of results.
        """

        params = self.get_set_params(locals())
        response = await self.request("gifts.get", params)
        model = GetResponse
        return model(**response).response


__all__ = ("GiftsCategory",)
