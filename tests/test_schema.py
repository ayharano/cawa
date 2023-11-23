import pytest
from pydantic import BaseModel, ValidationError

from cawa.schemas import AddressSchema, CustomerSchema, TrimmedString


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
