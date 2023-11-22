from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select

from cawa.models import Location


def test_create_and_retrieve_location(session):
    before_new_location = datetime.utcnow()
    new_location = Location(  # Statue of Liberty
        latitude=Decimal('40.689247'),
        longitude=Decimal('74.044502'),
    )
    session.add(new_location)
    session.commit()

    location = session.scalar(
        select(Location)
        .where(
            Location.latitude == Decimal('40.689247'),
            Location.longitude == Decimal('74.044502'),
        )
    )

    assert location.latitude == Decimal('40.689247')
    assert location.longitude == Decimal('74.044502')
    assert location.created > before_new_location
    assert location.updated > location.created


def test_can_create_duplicate_location(session):
    first_location = Location(  # Statue of Liberty
        latitude=Decimal('40.689247'),
        longitude=Decimal('74.044502'),
    )
    session.add(first_location)
    session.commit()
    session.refresh(first_location)

    second_location = Location(  # Statue of Liberty
        latitude=Decimal('40.689247'),
        longitude=Decimal('74.044502'),
    )
    session.add(second_location)
    session.commit()
    session.refresh(second_location)

    count = session.scalar(
        select(func.count('*'))
        .select_from(Location)
        .where(
            Location.latitude == Decimal('40.689247'),
            Location.longitude == Decimal('74.044502'),
        )
    )

    assert count == 2
    geodesic_distance = first_location.geodesic_distance(second_location)
    great_circle_distance = second_location.great_circle_distance(first_location)
    assert geodesic_distance == great_circle_distance
    assert geodesic_distance.miles == 0
    assert great_circle_distance.km == 0


def test_location_distance_for_different_locations(session):
    krakatoa = Location(  # Krakatoa
        latitude=Decimal('-6.101944'),
        longitude=Decimal('105.422778'),
    )
    session.add(krakatoa)
    session.commit()
    session.refresh(krakatoa)

    pompeii = Location(  # Pompeii
        latitude=Decimal('40.75'),
        longitude=Decimal('14.486111'),
    )
    session.add(pompeii)
    session.commit()
    session.refresh(pompeii)

    geodesic_distance = krakatoa.geodesic_distance(pompeii)
    great_circle_distance = pompeii.great_circle_distance(krakatoa)
    assert geodesic_distance != great_circle_distance
    assert 6540 < geodesic_distance.miles < geodesic_distance.km < 10530
    assert 6540 < great_circle_distance.miles < great_circle_distance.km < 10530
    assert great_circle_distance.miles < geodesic_distance.miles
