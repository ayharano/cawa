from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import generic_repr

from .base import TimestampedBase


@generic_repr
class Customer(TimestampedBase):
    __tablename__ = 'customer'
    __table_args__ = (
        CheckConstraint(
            "NOT(TRIM( full_name ) LIKE '')"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(1023))

    address: Mapped['Address'] = relationship(
        back_populates='customer',
        cascade='all, delete-orphan',
        single_parent=True,
    )
