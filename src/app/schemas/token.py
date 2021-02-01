from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
