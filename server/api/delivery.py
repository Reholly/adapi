from typing import List

from fastapi import APIRouter

from db.models import Delivery
from db.session import session
from server.schemas.delivery import DeliveryOut

router = APIRouter()


@router.get('/delivery', response_model=List[DeliveryOut])
def get_delivery():
    with session() as s:
        return s.query(Delivery).all()
