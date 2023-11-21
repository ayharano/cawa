from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import generic_repr

from .base import TimestampedBase


@generic_repr
class User(TimestampedBase):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool]
