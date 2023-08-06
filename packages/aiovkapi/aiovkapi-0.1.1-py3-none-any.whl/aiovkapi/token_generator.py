import typing

import pydantic

__all__ = (
    'Token',
    'TokenGenerator',
)


class Token(pydantic.BaseModel):
    access_token: str
    client_id: typing.Optional[int] = None
    client_secret: typing.Optional[str] = None
    user_agent: str = 'okhttp/3.12.1'

    def _ensured(self) -> str:
        return self.access_token[:4] + "****" + self.access_token[-4:]

    def __repr__(self) -> str:
        return f"Token(access_token={self._ensured()},client_id={self.client_id},user_agent={self.user_agent})"

    def __str__(self):
        return "Access token for VK"


class TokenGenerator:

    def __init__(
            self,
            *tokens: Token
    ):
        self._tokens = tokens
        self._index = 0

    @property
    def index(self) -> int:
        if self._index + 1 == len(self._tokens):
            self._index = 0
        else:
            self._index += 1
        return self._index

    def get_token(self) -> Token:
        return self._tokens[self.index]

    def __repr__(self) -> str:
        return f"TokenGenerator({self._index + 1}/{len(self._tokens)})"
