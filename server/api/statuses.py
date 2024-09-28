from typing import List

from fastapi import APIRouter

from db.models import Status
from db.session import session
from server.schemas.status import StatusOut

router = APIRouter()


@router.get('/statuses', response_model=List[StatusOut])
def get_statuses():
    with session() as s:
        return s.query(Status).all()
