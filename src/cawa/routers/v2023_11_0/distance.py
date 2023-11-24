from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from cawa.database import get_session
from cawa.models import Address, Customer, User, Warehouse
from cawa.routers.v2023_11_0.auth import get_current_active_user
from cawa.schemas import DistanceSchema


router = APIRouter(prefix='/distance', tags=['distance'])

Session = Annotated[Session, Depends(get_session)]

CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]


geodesic = 'geodesic'
Geodesic = Literal[geodesic]
great_circle = 'great-circle'
GreatCircle = Literal[great_circle]
DistanceMethod = Literal[Geodesic, GreatCircle]


@router.get('/', response_model=DistanceSchema, status_code=200)
def calculate_distance(
    customer_id: int,
    warehouse_id: int,
    session: Session,
    current_active_user: CurrentActiveUser,
    method: Annotated[DistanceMethod, Query()] = geodesic,
):
    customer = session.scalar(
        select(Customer)
        .where(Customer.id == customer_id)
        .options(
            joinedload(Customer.address)
            .joinedload(Address.location)
        )
    )

    if (
        not customer
        or not customer.address
        or not customer.address.location
    ):
        raise HTTPException(status_code=404, detail=f'Customer {customer_id} not found.')

    warehouse = session.scalar(
        select(Warehouse)
        .where(Warehouse.id == warehouse_id)
        .options(
            joinedload(Warehouse.address)
            .joinedload(Address.location)
        )
    )

    if (
        not warehouse
        or not warehouse.address
        or not warehouse.address.location
    ):
        raise HTTPException(status_code=404, detail=f'Warehouse {warehouse_id} not found.')

    customer_location = customer.address.location
    warehouse_location = warehouse.address.location

    distance_method = {
        geodesic: customer_location.geodesic_distance,
        great_circle: customer_location.great_circle_distance,
    }.get(method)

    distance_object = distance_method(warehouse_location)

    return {
        'miles': distance_object.miles,
        'kilometers': distance_object.km,
    }
