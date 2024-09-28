from typing import List, Optional

from fastapi import APIRouter, Query

from db import Author
from db.session import session
from server.schemas.author import AuthorIn, AuthorInPartial, AuthorOut

router = APIRouter()


@router.get('/authors', response_model=List[AuthorOut])
def get_authors(
    rating: Optional[float] = Query(None, ge=0, le=5),
    reliability: Optional[bool] = None,
):
    with session() as s:
        q = s.query(Author)
        if rating:
            q = q.filter(Author.rating >= rating)
        if reliability:
            q = q.filter(Author.reliability.is_(reliability))
        return q.all()


@router.post('/authors', response_model=AuthorOut)
def create_author(author_in: AuthorIn):
    with session() as s:
        author = s.merge(Author(**author_in.dict()))
        s.commit()
        return author


@router.put('/authors/{author_id}', response_model=AuthorOut)
def update_author(author_id: int, author_in: AuthorInPartial):
    with session() as s:
        author = s.merge(Author(**author_in.dict(exclude_unset=True), id=author_id))
        s.commit()
        return author
