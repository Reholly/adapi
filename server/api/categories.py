from typing import List

from fastapi import APIRouter

from db.models import Category
from db.session import session
from server.schemas.category import CategoryOut

router = APIRouter()


@router.get('/categories', response_model=List[CategoryOut])
def get_categories():
    with session() as s:
        return s.query(Category).all()
