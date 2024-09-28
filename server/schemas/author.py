from typing import Optional

from pydantic import Field, validator

from .common import APIModel


class AuthorBase(APIModel):
    login: str = Field(max_length=20)
    email: str


class AuthorOut(AuthorBase):
    id: int
    open_advertisement: int
    close_advertisement: int
    rating: Optional[float] = Field(ge=0, le=5)
    reliability: bool

    @validator('rating')
    def rating_round(cls, v):
        if v is None:
            return v
        return round(v, 1)


class AuthorIn(AuthorBase):
    pass


class AuthorInPartial(AuthorBase):
    login: Optional[str] = Field(..., max_length=20)
    email: Optional[str]
