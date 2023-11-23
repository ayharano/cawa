from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from cawa.database import get_session
from cawa.models import Address, Warehouse, User
from cawa.routers.v2023_11_0.auth import get_current_active_user
from cawa.schemas import AddressSchema, WarehousePublic, WarehouseSchema


router = APIRouter(prefix='/warehouses', tags=['warehouses'])

Session = Annotated[Session, Depends(get_session)]

CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]


@router.post('/', response_model=WarehousePublic, status_code=201)
def create_warehouse(
    warehouse: WarehouseSchema,
    session: Session,
    current_active_user: CurrentActiveUser,
):
    address_data = {
        field_name: getattr(warehouse, field_name)
        for field_name in AddressSchema.model_fields
    }
    db_address = Address(**address_data)
    session.add(db_address)
    session.commit()
    session.refresh(db_address)

    db_warehouse = Warehouse(
        code=warehouse.code,
        address=db_address
    )
    session.add(db_warehouse)
    session.commit()
    session.refresh(db_warehouse)

    result = {
        field_name: getattr(db_address, field_name)
        for field_name in AddressSchema.model_fields
    }
    result.update({
        field_name: getattr(db_warehouse, field_name)
        for field_name in ('id', 'code')
    })

    return result
