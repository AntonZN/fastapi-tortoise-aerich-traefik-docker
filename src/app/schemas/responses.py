from pydantic import BaseModel


class HTTPBadRequest(BaseModel):
    detail: str


class HTTPForbidden(BaseModel):
    detail: str


class HTTPUnauthorized(BaseModel):
    detail: str


class HTTPNotFound(BaseModel):
    detail: str
