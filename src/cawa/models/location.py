from decimal import Decimal
from typing import Self

from geopy.distance import GeodesicDistance, GreatCircleDistance
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import generic_repr

from .base import TimestampedBase


@generic_repr
class Location(TimestampedBase):
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[Decimal] = mapped_column(Numeric(precision=7, asdecimal=True))
    longitude: Mapped[Decimal] = mapped_column(Numeric(precision=7, asdecimal=True))

    def as_tuple(self: Self) -> tuple[Decimal, Decimal]:
        return (self.latitude, self.longitude)

    def geodesic_distance(self: Self, another: Self) -> GeodesicDistance:
        current_location = self.as_tuple()
        another_location = another.as_tuple()
        return GeodesicDistance(current_location, another_location)

    def great_circle_distance(self: Self, another: Self) -> GreatCircleDistance:
        current_location = self.as_tuple()
        another_location = another.as_tuple()
        return GreatCircleDistance(current_location, another_location)
