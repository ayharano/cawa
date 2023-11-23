from datetime import datetime

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from cawa.models import Address, Customer


def test_create_and_retrieve_customer(session):
    address = Address(
        address='221b Baker Street',
        city='London',
        state='',
        country='UK',
        postal_code='',
    )
    session.add(address)
    session.commit()
    session.refresh(address)

    before_new_customer = datetime.utcnow()
    new_customer = Customer(
        full_name='Sherlock Holmes',
        address=address,
    )
    session.add(new_customer)
    session.commit()

    customer = session.scalar(
        select(Customer)
        .where(
            Customer.full_name == 'Sherlock Holmes',
        )
    )

    assert customer.full_name == 'Sherlock Holmes'
    assert customer.address == address
    assert customer.created > before_new_customer
    assert customer.updated > customer.created
