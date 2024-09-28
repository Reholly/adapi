from typing import List

from fastapi import APIRouter

from db.models import ReasonClosing
from db.session import session
from server.schemas.reason_closing import ReasonClosingOut

router = APIRouter()


@router.get('/reason_closing', response_model=List[ReasonClosingOut])
def get_reasons_closing():
    with session() as s:
        return s.query(ReasonClosing).all()
