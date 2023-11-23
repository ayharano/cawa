from datetime import datetime
from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from cawa.models import Address, Location


def test_create_and_retrieve_location(session):
    address = Address(
        address='Statue of Liberty',
        city='New York',
        state='NY',
        country='USA',
        postal_code='10004',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    before_new_location = datetime.utcnow()
    new_location = Location(  # Statue of Liberty
        latitude=Decimal('40.689247'),
        longitude=Decimal('74.044502'),
        address=address,
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
    assert location.address_id == address.id
    assert location.address == address
    assert location.created > before_new_location
    assert location.updated > location.created


def test_location_instance_is_deleted_when_address_instance_is_deleted(session):
    address = Address(
        address='Grand Canyon',
        city='',
        state='',
        country='USA',
        postal_code='',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    location = Location(  # Grand Canyon
        latitude=Decimal('36.3'),
        longitude=Decimal('-112.6'),
        address=address,
    )
    session.add(location)
    session.commit()
    session.refresh(location)

    count_before_delete = session.scalar(
        select(func.count('*'))
        .select_from(Location)
    )
    assert count_before_delete == 1

    session.delete(address)
    session.commit()

    count_after_delete = session.scalar(
        select(func.count('*'))
        .select_from(Location)
    )
    assert count_after_delete == 0


def test_cannot_create_duplicate_location_for_the_same_address_instance(session):
    address = Address(
        address='Statue of Liberty',
        city='New York',
        state='NY',
        country='USA',
        postal_code='10004',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    first_location = Location(  # Statue of Liberty
        latitude=Decimal('40.689247'),
        longitude=Decimal('74.044502'),
        address=address,
    )
    session.add(first_location)
    session.commit()
    session.refresh(first_location)

    second_location = Location(  # Statue of Liberty using the same Address instance
        latitude=Decimal('40.689247'),
        longitude=Decimal('74.044502'),
        address=address,
    )
    session.add(second_location)
    with pytest.raises(IntegrityError):
        session.commit()


def test_location_distance_for_different_locations(session):
    krakatoa_address = Address(
        address='Krakatau',
        city='',
        state='',
        country='Indonesia',
        postal_code='',
    )
    session.add(krakatoa_address)
    session.commit()
    session.refresh(krakatoa_address)
    krakatoa = Location(  # Krakatoa
        latitude=Decimal('-6.101944'),
        longitude=Decimal('105.422778'),
        address=krakatoa_address,
    )
    session.add(krakatoa)
    session.commit()
    session.refresh(krakatoa)

    pompeii_address = Address(
        address='Pompeii',
        city='',
        state='Campania',
        country='Italia',
        postal_code='',
    )
    session.add(pompeii_address)
    session.commit()
    session.refresh(pompeii_address)
    pompeii = Location(  # Pompeii
        latitude=Decimal('40.75'),
        longitude=Decimal('14.486111'),
        address=pompeii_address,
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
