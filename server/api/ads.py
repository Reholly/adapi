from typing import List, Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from db import Ad, Category, ReasonClosing, Status
from db.session import session
from server.api.common import verify_ad_in
from server.schemas.ad import AdNewIn, AdOut, AdUpdateIn

router = APIRouter()


@router.get('/ads', response_model=List[AdOut])
def get_ads(
    location: Optional[str] = None,
    category: Optional[str] = None,
    price: Optional[float] = None,
):
    with session() as s:
        q = s.query(Ad)
        if location or category or price:
            q = q.filter(Ad.status_id != Status.get_id_by_name('Close'))
        if location:
            q = q.filter(Ad.location == location.strip().title())
        if category:
            q = q.join(Category).filter(Category.category_name == category)
        if price:
            q = q.filter(Ad.price <= price)

        return q.all()


@router.get('/ads/{ad_id}', response_model=AdOut)
def get_ad(ad_id: int):
    with session() as s:
        return _get_ad_or_raise(ad_id, s)


@router.post('/ads', response_model=AdOut)
def create_ad(ad_in: AdNewIn):
    with session() as s:
        verify_ad_in(ad_in, None, s)
        ad = Ad(
            **ad_in.dict(),
            status_id=Status.get_id_by_name('Open'),
            is_sold=False,
        )
        ad = s.merge(ad)
        s.flush()
        ad.author.open_advertisement += 1
        return _recalc_author_rating(ad, s)


@router.put('/ads/{ad_id}', response_model=AdOut)
def update_ad(ad_id: int, ad_in: AdUpdateIn):
    with session() as s:
        db_ad = _get_ad_or_raise(ad_id, s)
        verify_ad_in(ad_in, db_ad, s)

        inp = ad_in.dict(exclude_unset=True)
        status_changed = 'status_id' in inp and ad_in.status_id != db_ad.status_id

        for k, v in inp.items():
            setattr(db_ad, k, v)
        s.flush()

        if status_changed and db_ad.status_id == Status.get_id_by_name('Close'):
            db_ad.is_sold = db_ad.reason_closing_id == ReasonClosing.get_id_by_name(
                'Sold Here'
            )
            db_ad.author.open_advertisement -= 1
            db_ad.author.close_advertisement += 1

        return _recalc_author_rating(db_ad, s)


@router.delete('/ads/{ad_id}', status_code=201)
def delete_ad(ad_id: int):
    with session() as s:
        db_ad = _get_ad_or_raise(ad_id, s)
        if db_ad.status.status_name != 'Close':
            db_ad.author.open_advertisement -= 1
            db_ad.author.close_advertisement += 1
        s.delete(db_ad)


def _get_ad_or_raise(ad_id: int, s: Session) -> Ad:
    db_ad = s.query(Ad).get(ad_id)
    if not db_ad:
        raise HTTPException(status_code=404)
    return db_ad


def _recalc_author_rating(db_ad: Ad, s: Session) -> Ad:
    author_id = db_ad.author_id

    author_sold_ads = (
        s.query(Ad).filter(Ad.author_id == author_id, Ad.is_sold.is_(True)).all()
    )

    rating = None
    if author_sold_ads:
        rating = sum(ad.score for ad in author_sold_ads) / len(author_sold_ads)

    db_ad.author.rating = rating
    db_ad.author.reliability = rating is not None and rating >= 4

    return db_ad
