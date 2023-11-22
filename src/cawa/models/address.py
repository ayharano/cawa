from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import generic_repr

from .base import TimestampedBase


@generic_repr
class Address(TimestampedBase):
    __tablename__ = 'address'
    __table_args__ = (
        CheckConstraint(
            "NOT("
            " TRIM( address ) LIKE ''"
            " AND TRIM( city ) LIKE ''"
            " AND TRIM( state ) LIKE ''"
            " AND TRIM( country ) LIKE ''"
            " AND TRIM( postal_code ) LIKE ''"
            ")"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(1023))
    city: Mapped[str] = mapped_column(String(1023))
    state: Mapped[str] = mapped_column(String(1023))
    country: Mapped[str] = mapped_column(String(255))
    postal_code: Mapped[str] = mapped_column(String(15))
