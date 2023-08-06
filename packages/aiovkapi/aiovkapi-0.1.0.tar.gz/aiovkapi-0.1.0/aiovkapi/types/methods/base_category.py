import typing

if typing.TYPE_CHECKING:
    import aiovkapi

T = typing.TypeVar("T")


class BaseCategory:

    def __init__(self, api: "aiovkapi.API"):
        self.api = api

    @classmethod
    def get_set_params(cls, _locals: dict) -> typing.Any:
        exclude_params = _locals.copy()
        exclude_params.update(_locals["kwargs"])
        exclude_params.pop("kwargs")
        return {
            k[1:] if k.startswith("_") else k: v
            for k, v in exclude_params.items()
            if k != "self" and v is not None
        }

    @classmethod
    def get_model(
            cls,
            dependent: typing.Tuple[
                typing.Tuple[typing.Tuple[typing.Union[str, typing.List[str]], ...], T], ...
            ],
            default: T,
            params: dict,
    ) -> T:
        """Choices model depending on params"""
        for items in sorted(dependent, key=lambda x: len(x[0])):
            keys, model = items
            for key in keys:
                if isinstance(key, str) and params.get(key) is None:
                    break
                elif isinstance(key, list) and params.get(key[0]) not in key[1:]:
                    break
            else:
                return model

        return default

    async def request(self, method_name: str, params: dict) -> typing.Any:
        return await self.api.method(
            method_name,
            raw=True,
            **params
        )
