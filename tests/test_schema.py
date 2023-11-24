import json
from decimal import Decimal

import pytest
from pydantic import BaseModel, ValidationError

from cawa.schemas import (
    AddressSchema,
    CustomerSchema,
    DistanceSchema,
    TrimmedString,
    WarehouseSchema,
)


def test_trimmedstring():
    class SingleField(BaseModel):
        field: TrimmedString

    instance = SingleField(field='\r\n\t something \t\r\n')
    assert instance.field == 'something'


def test_addressschema():
    schema = AddressSchema(
        address='  760 United Nations Plaza\t\n',
        city='\tNew York City\n',
        state=' NY ',
        country='\r\nUSA\r\n',
        postal_code='10017',
    )
    assert schema.address == '760 United Nations Plaza'
    assert schema.city == 'New York City'
    assert schema.state == 'NY'
    assert schema.country == 'USA'
    assert schema.postal_code == '10017'


def test_addressschema_does_not_accept_whitespace_only_field_data():
    with pytest.raises(ValidationError):
        AddressSchema(
            address='',
            city=' ',
            state='\t',
            country='\r\n',
            postal_code='\f\v',
        )


def test_customer():
    schema = CustomerSchema(
        full_name='\t\f\v John Doe\r\n ',
        address='  760 United Nations Plaza\t\n',
        city='\tNew York City\n',
        state=' NY ',
        country='\r\nUSA\r\n',
        postal_code='10017',
    )
    assert schema.full_name == 'John Doe'
    assert schema.address == '760 United Nations Plaza'
    assert schema.city == 'New York City'
    assert schema.state == 'NY'
    assert schema.country == 'USA'
    assert schema.postal_code == '10017'


def test_customerschema_does_not_accept_whitespace_only_full_name_value():
    with pytest.raises(ValidationError):
        CustomerSchema(
            full_name='\r\n\f\v \r\n',
            address='Pacific Ocean',
            city='',
            state='',
            country='',
            postal_code='',
        )


def test_warehouse():
    schema = WarehouseSchema(
        code='\t\f\v port-usa-ca-losangeles\r\n ',
        address='  Port of Los Angeles\t\n',
        city='\nLos Angeles\t',
        state='  CA ',
        country='\r\nUSA\r\n',
        postal_code='\t \n',
    )
    assert schema.code == 'port-usa-ca-losangeles'
    assert schema.address == 'Port of Los Angeles'
    assert schema.city == 'Los Angeles'
    assert schema.state == 'CA'
    assert schema.country == 'USA'
    assert schema.postal_code == ''


def test_warehouseschema_does_not_accept_whitespace_only_code_value():
    with pytest.raises(ValidationError):
        WarehouseSchema(
            full_name='\r\n  \r\n\f\v ',
            address='Atlantic Ocean',
            city='',
            state='',
            country='',
            postal_code='',
        )


def test_distance():
    schema = DistanceSchema(
        kilometers=123456.78901,
        miles=109876.54321,
    )
    assert schema.kilometers == Decimal('123456.789')
    assert schema.miles == Decimal('109876.543')


def test_distance_json():
    schema = DistanceSchema(
        kilometers=123456.78901,
        miles=109876.54321,
    )
    json_str = schema.model_dump_json()
    json_ = json.loads(json_str)
    assert json_['kilometers'] == '123456.789'
    assert json_['miles'] == '109876.543'
