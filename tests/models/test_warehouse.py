from datetime import datetime

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from cawa.models import Address, Warehouse


def test_create_and_retrieve_warehouse(session):
    address = Address(
        address='Port of Los Angeles',
        city='Los Angeles',
        state='CA',
        country='USA',
        postal_code='',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    before_new_warehouse = datetime.utcnow()
    new_warehouse = Warehouse(
        code='port-usa-ca-losangeles',
        address=address,
    )
    session.add(new_warehouse)
    session.commit()

    warehouse = session.scalar(
        select(Warehouse)
        .where(
            Warehouse.code == 'port-usa-ca-losangeles',
        )
    )

    assert warehouse.code == 'port-usa-ca-losangeles'
    assert warehouse.address == address
    assert warehouse.created > before_new_warehouse
    assert warehouse.updated > warehouse.created


def test_cannot_create_duplicate_warehouse(session):
    new_warehouse = Warehouse(
        code='port-usa-tx-houston',
    )
    session.add(new_warehouse)
    session.commit()

    new_warehouse = Warehouse(
        code='port-usa-tx-houston',
    )
    session.add(new_warehouse)
    with pytest.raises(IntegrityError):
        session.commit()
