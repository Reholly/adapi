from decimal import Decimal

from .common import APIModel


class DeliveryBase(APIModel):
    id: int
    delivery_type: str
    price: Decimal


class DeliveryOut(DeliveryBase):
    pass
