from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy_utils import Timestamp, generic_repr


class Base(DeclarativeBase):
    pass


class TimestampedBase(Base, Timestamp):
    __abstract__ = True


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
