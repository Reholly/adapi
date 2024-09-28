from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import DeclBase
from db.session import session


class Ad(DeclBase):
    __tablename__ = 'ad'

    id = sa.Column(sa.Integer, primary_key=True)
    category_id = sa.Column(sa.Integer, sa.ForeignKey('category.id'), nullable=False)
    title = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=False)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('author.id'), nullable=False)
    price = sa.Column(sa.DECIMAL, nullable=False)
    status_id = sa.Column(sa.Integer, sa.ForeignKey('status.id'), nullable=False)
    publish_date = sa.Column(sa.DateTime, default=datetime.now, nullable=False)
    location = sa.Column(sa.String, nullable=False)
    delivery_flag = sa.Column(sa.Boolean, nullable=False)
    delivery_type_id = sa.Column(
        sa.Integer, sa.ForeignKey('delivery.id'), nullable=True
    )
    delivery_price = sa.Column(sa.DECIMAL)

    reason_closing_id = sa.Column(
        sa.Integer, sa.ForeignKey('reason_closing.id'), nullable=False
    )
    is_sold = sa.Column(sa.Boolean, nullable=False)
    score = sa.Column(sa.Integer, nullable=True)

    category = relationship('Category', uselist=False)
    status = relationship('Status', uselist=False)
    delivery_type = relationship('Delivery', uselist=False)
    author = relationship('Author', lazy='joined')
    reason_closing = relationship('ReasonClosing', uselist=False)


class Category(DeclBase):
    __tablename__ = 'category'

    id = sa.Column(sa.Integer, primary_key=True)
    category_name = sa.Column(sa.String, default='', nullable=False)


class Author(DeclBase):
    __tablename__ = 'author'

    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    open_advertisement = sa.Column(sa.Integer, default=0, nullable=False)
    close_advertisement = sa.Column(sa.Integer, default=0, nullable=False)
    rating = sa.Column(sa.DECIMAL, default=0)
    reliability = sa.Column(sa.Boolean, default=False, nullable=False)


class Status(DeclBase):
    __tablename__ = 'status'

    id = sa.Column(sa.Integer, primary_key=True)
    status_name = sa.Column(sa.String, nullable=False)

    @classmethod
    def get_id_by_name(cls, name: str) -> int:
        with session() as s:
            status = s.query(cls).filter(cls.status_name == name).first()
            if status is None:
                raise ValueError(f'No such status: {name}')
            return status.id


class Delivery(DeclBase):
    __tablename__ = 'delivery'

    id = sa.Column(sa.Integer, primary_key=True)
    delivery_type = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.DECIMAL, nullable=False)


class ReasonClosing(DeclBase):
    __tablename__ = 'reason_closing'

    id = sa.Column(sa.Integer, primary_key=True)
    reason_name = sa.Column(sa.String, nullable=False)

    @classmethod
    def get_id_by_name(cls, name: str) -> int:
        with session() as s:
            reason = s.query(cls).filter(cls.reason_name == name).first()
            if reason is None:
                raise ValueError(f'No such reason: {name}')
            return reason.id
