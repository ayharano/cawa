import pytest
from pydantic import BaseModel, ValidationError

from cawa.schemas import AddressSchema, TrimmedString


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
