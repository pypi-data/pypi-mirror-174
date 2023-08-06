import pydantic
from pydantic import Extra


class BaseModel(pydantic.BaseModel):

    class Config:
        extra = Extra.allow

