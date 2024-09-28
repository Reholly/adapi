from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Ad, Author, Category, Delivery, ReasonClosing, Status
from server.schemas.ad import AdNewIn, AdUpdateClosedIn, AdUpdateIn, AdUpdateOpenedIn


def verify_ad_in(
    ad_in: Union[AdNewIn, AdUpdateClosedIn, AdUpdateOpenedIn],
    db_ad: Optional[Ad],
    s: Session,
):
    if isinstance(ad_in, AdNewIn):
        _verify_new_ad(ad_in, s)
    elif isinstance(ad_in, AdUpdateOpenedIn):
        _verify_update_ad(ad_in, db_ad, s)
    else:
        _verify_closed_ad_update(ad_in, db_ad)


def _verify_new_ad(ad_in: AdNewIn, s):
    _verify_category(ad_in.category_id, s)
    _verify_author(ad_in.author_id, s)
    _verify_delivery(ad_in.delivery_type_id, s)


def _verify_update_ad(ad_in: AdUpdateIn, db_ad: Ad, s):
    closed_id = Status.get_id_by_name('Close')

    if db_ad.status_id == closed_id:
        raise HTTPException(
            status_code=400, detail='Only rating can be changed for a closed Ad'
        )

    if ad_in.category_id is not None:
        _verify_category(ad_in.category_id, s)

    if ad_in.delivery_type_id is not None:
        _verify_delivery(ad_in.delivery_type_id, s)

    if ad_in.status_id is not None:
        _verify_status(ad_in.status_id, s)

    if ad_in.status_id == closed_id:
        _verify_closing_reason(ad_in.reason_closing_id, s)


def _verify_closed_ad_update(ad_in: AdUpdateClosedIn, db_ad: Optional[Ad]):
    if not db_ad or not db_ad.is_sold:
        raise HTTPException(
            status_code=400, detail=f'Unable to set a score to ad, it is not sold'
        )
    if not 1 <= ad_in.score <= 5:
        raise HTTPException(status_code=400, detail='Bad score')


def _verify_category(category_id: int, s: Session) -> None:
    if not s.query(Category).get(category_id):
        raise HTTPException(
            status_code=400, detail=f'Unknown Category id: {category_id}'
        )


def _verify_author(author_id: int, s: Session) -> None:
    if not s.query(Author).get(author_id):
        raise HTTPException(status_code=400, detail=f'Unknown Author id: {author_id}')


def _verify_status(status_id: int, s: Session) -> None:
    if not s.query(Status).get(status_id):
        raise HTTPException(status_code=400, detail=f'Unknown Status id: {status_id}')


def _verify_delivery(delivery_type_id: int, s: Session) -> None:
    if not s.query(Delivery).get(delivery_type_id):
        raise HTTPException(
            status_code=400, detail=f'Unknown Delivery Type id: {delivery_type_id}'
        )


def _verify_closing_reason(reason_closing_id: Optional[int], s: Session) -> None:
    if not reason_closing_id:
        raise HTTPException(
            status_code=400,
            detail='A closing reason must be passed while closing the Ad',
        )
    if not s.query(ReasonClosing).get(reason_closing_id):
        raise HTTPException(
            status_code=400, detail=f'Unknown Closing Reason id: {reason_closing_id}'
        )
