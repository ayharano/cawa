from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from cawa.database import get_session
from cawa.models import Address, Customer, User
from cawa.routers.v2023_11_0.auth import get_current_active_user
from cawa.schemas import AddressSchema, CustomerPublic, CustomerSchema


router = APIRouter(prefix='/customers', tags=['customers'])

Session = Annotated[Session, Depends(get_session)]

CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]


@router.post('/', response_model=CustomerPublic, status_code=201)
def create_customer(
    customer: CustomerSchema,
    session: Session,
    current_active_user: CurrentActiveUser,
):
    address_data = {
        field_name: getattr(customer, field_name)
        for field_name in AddressSchema.model_fields
    }
    db_address = Address(**address_data)
    session.add(db_address)
    session.commit()
    session.refresh(db_address)

    db_customer = Customer(
        full_name=customer.full_name,
        address=db_address
    )
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)

    result = {
        field_name: getattr(db_address, field_name)
        for field_name in AddressSchema.model_fields
    }
    result.update({
        field_name: getattr(db_customer, field_name)
        for field_name in ('id', 'full_name')
    })

    return result
