from datetime import datetime

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from cawa.models import Address, Customer, Warehouse


def test_create_and_retrieve_address(session):
    before_new_address = datetime.utcnow()
    new_address = Address(
        address='Statue of Liberty',
        city='New York',
        state='NY',
        country='USA',
        postal_code='10004',
    )
    session.add(new_address)
    session.commit()

    address = session.scalar(
        select(Address)
        .where(
            Address.country == 'USA',
            Address.postal_code == '10004',
        )
    )

    assert address.address == 'Statue of Liberty'
    assert address.city == 'New York'
    assert address.state == 'NY'
    assert address.country == 'USA'
    assert address.postal_code == '10004'
    assert address.created > before_new_address
    assert address.updated > address.created


def test_cannot_create_fully_empty_address(session):
    fully_empty_address = Address(  # Fully empty address
        address='',  # empty
        city=' ',  # single whitespace
        state='   ',  # double whitespace
        country='    ',  # triple whitespace
        postal_code='',  # empty
    )
    session.add(fully_empty_address)
    with pytest.raises(IntegrityError):
        session.commit()


def test_can_create_duplicate_address(session):
    first_address = Address(  # Alcatraz
        address='Alcatraz Island',
        city='San Francisco',
        state='CA',
        country='USA',
        postal_code='94133',
    )
    session.add(first_address)
    session.commit()
    session.refresh(first_address)

    second_address = Address(  # Alcatraz
        address='Alcatraz Island',
        city='San Francisco',
        state='CA',
        country='USA',
        postal_code='94133',
    )
    session.add(second_address)
    session.commit()
    session.refresh(second_address)

    count = session.scalar(
        select(func.count('*'))
        .select_from(Address)
        .where(
            Address.address == 'Alcatraz Island',
        )
    )

    assert count == 2


def test_address_instance_cannot_simultaneously_relate_to_a_customer_and_a_warehouse(session):
    warehouse = Warehouse(
        code='airport-usa-nynj-jfk',
    )
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)

    customer = Customer(
        full_name='Viktor Navorski',
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)

    address = Address(
        address='John F. Kennedy International Airport',
        city='',
        state='',
        country='USA',
        postal_code='',
        customer=customer,
        warehouse=warehouse,
    )
    session.add(address)
    with pytest.raises(IntegrityError):
        session.commit()


def test_address_instance_is_deleted_when_related_customer_instance_is_deleted(session):
    address = Address(
        address='1600 Pennsylvania Avenue',
        city='Washington',
        state='DC',
        country='USA',
        postal_code='20500',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    customer = Customer(
        full_name='Barack Obama',
        address=address,
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)

    count_before_delete = session.scalar(
        select(func.count('*'))
        .select_from(Address)
    )
    assert count_before_delete == 1

    session.delete(customer)
    session.commit()

    count_after_delete = session.scalar(
        select(func.count('*'))
        .select_from(Address)
    )
    assert count_after_delete == 0


def test_address_instance_is_deleted_when_related_warehouse_instance_is_deleted(session):
    address = Address(
        address='Port of Long Beach',
        city='Long Beach',
        state='CA',
        country='USA',
        postal_code='',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    warehouse = Warehouse(
        code='port-usa-ca-long-beach',
        address=address,
    )
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)

    count_before_delete = session.scalar(
        select(func.count('*'))
        .select_from(Address)
    )
    assert count_before_delete == 1

    session.delete(warehouse)
    session.commit()

    count_after_delete = session.scalar(
        select(func.count('*'))
        .select_from(Address)
    )
    assert count_after_delete == 0
