from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import generic_repr

from .base import TimestampedBase


@generic_repr
class Warehouse(TimestampedBase):
    __tablename__ = 'warehouse'
    __table_args__ = (
        UniqueConstraint('code'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(1023))

    address: Mapped['Address'] = relationship(
        back_populates='warehouse',
        cascade='all, delete-orphan',
        single_parent=True,
    )
