from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

from pydantic import Field, validator

from .common import APIModel


class AdBase(APIModel):
    category_id: int
    author_id: int
    title: str = Field(max_length=75)
    text: str = Field(max_length=300)
    price: Decimal
    location: str = Field(min_length=4)
    delivery_flag: bool = False
    delivery_type_id: Optional[int]
    delivery_price: Optional[Decimal]


class AdOut(AdBase):
    id: int
    status_id: int
    publish_date: datetime
    reason_closing_id: Optional[int]
    is_sold: bool
    score: Optional[int]


class AdNewIn(AdBase):
    @validator('location')
    def capitalize_location(cls, v):
        if v is None:
            return v
        return v.strip().title()


class AdUpdateOpenedIn(APIModel):
    category_id: Optional[int]
    status_id: Optional[int]
    title: Optional[str]
    text: Optional[str]
    price: Optional[Decimal]
    location: Optional[str] = Field(None, min_length=4)
    delivery_flag: Optional[bool]
    delivery_type_id: Optional[int]
    reason_closing_id: Optional[int]

    @validator('location')
    def capitalize_location(cls, v):
        if v is None:
            return v
        return v.strip().title()


class AdUpdateClosedIn(APIModel):
    score: int


AdUpdateIn = Union[AdUpdateClosedIn, AdUpdateOpenedIn]
