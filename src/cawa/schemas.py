from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.functional_validators import AfterValidator

from cawa.constants import DIGITS_OF_PRECISION_AFTER_DECIMAL_POINT


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Adapted from https://docs.pydantic.dev/2.5/concepts/validators/#annotated-validators
def strip_string(raw: str) -> str:
    return raw.strip()


def non_empty_trimmed_string(trimmed: str) -> str:
    if trimmed == '':
        raise ValueError('must not be empty or contain only whitespace characters')
    return trimmed



TrimmedString = Annotated[str, AfterValidator(strip_string)]
NonEmptyTrimmedString = Annotated[TrimmedString, AfterValidator(non_empty_trimmed_string)]


def limit_into_decimal(
    value: int | str | tuple[int, int, int] | float | Decimal,
) -> Decimal:
    as_decimal = Decimal(value)
    rounded_value = round(as_decimal, DIGITS_OF_PRECISION_AFTER_DECIMAL_POINT)
    return rounded_value


LimitedDecimal = Annotated[Decimal, AfterValidator(limit_into_decimal)]


class AddressSchema(BaseModel):
    address: TrimmedString
    city: TrimmedString
    state: TrimmedString
    country: TrimmedString
    postal_code: TrimmedString

    @model_validator(mode='after')
    def check_at_least_one_non_empty(self) -> 'AddressSchema':
        fields = (
            self.address,
            self.city,
            self.state,
            self.country,
            self.postal_code,
        )
        if not any(fields):
            raise ValueError('at least one of the Address fields must be filled in')
        return self


class CustomerSchema(AddressSchema):
    full_name: NonEmptyTrimmedString


class CustomerPublic(CustomerSchema):
    id: int


class WarehouseSchema(AddressSchema):
    code: NonEmptyTrimmedString


class WarehousePublic(WarehouseSchema):
    id: int


class DistanceSchema(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    kilometers: LimitedDecimal
    miles: LimitedDecimal
