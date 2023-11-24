from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
        CheckConstraint(
            "NOT("
            " customer_id IS NOT NULL"
            " AND warehouse_id IS NOT NULL"
            ")"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(1023))
    city: Mapped[str] = mapped_column(String(1023))
    state: Mapped[str] = mapped_column(String(1023))
    country: Mapped[str] = mapped_column(String(255))
    postal_code: Mapped[str] = mapped_column(String(15))

    location: Mapped['Location'] = relationship(
        back_populates='address',
        cascade='all, delete-orphan',
        single_parent=True,
    )

    customer_id: Mapped[int | None] = mapped_column(ForeignKey('customer.id'))
    customer: Mapped[Optional['Customer']] = relationship(back_populates='address')

    warehouse_id: Mapped[int | None] = mapped_column(ForeignKey('warehouse.id'))
    warehouse: Mapped[Optional['Warehouse']] = relationship(back_populates='address')
