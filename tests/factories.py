from datetime import datetime, timedelta

import factory

from cawa.models import Address, Customer, Location, User, Warehouse


class TimestampedBaseFactory(factory.Factory):
    created = factory.LazyFunction(datetime.utcnow)
    updated = factory.LazyAttribute(lambda obj: obj.created + timedelta(seconds=0.15))


class UserFactory(TimestampedBaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n+1)
    username = factory.Sequence(lambda n: f'user{n+1}')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    is_active = True


class LocationFactory(TimestampedBaseFactory):
    class Meta:
        model = Location

    class Params:
        # location_on_land tuple structure: (latitude, longitude, city, country, timezone)
        # more details: https://faker.readthedocs.io/en/master/providers/faker.providers.geo.html#faker.providers.geo.Provider.location_on_land
        location_on_land = factory.Faker('location_on_land')
        latitude_ = factory.LazyAttribute(lambda obj: obj.location_on_land[0])
        longitude_ = factory.LazyAttribute(lambda obj: obj.location_on_land[1])
        city = factory.LazyAttribute(lambda obj: obj.location_on_land[2])
        country = factory.LazyAttribute(lambda obj: obj.location_on_land[3])

    id = factory.Sequence(lambda n: n+1)
    latitude = factory.SelfAttribute('.latitude_')
    longitude = factory.SelfAttribute('.longitude_')
    address = factory.SubFactory(
        'tests.factories.AddressFactory',
        location=factory.SelfAttribute('..'),
        city=factory.SelfAttribute('..city'),
        country=factory.SelfAttribute('..country'),
    )
    address_id = factory.LazyAttribute(lambda obj: obj.address.id)


class AddressFactory(TimestampedBaseFactory):
    class Meta:
        model = Address

    class Params:
        # location_on_land tuple structure: (latitude, longitude, city, country, timezone)
        # more details: https://faker.readthedocs.io/en/master/providers/faker.providers.geo.html#faker.providers.geo.Provider.location_on_land
        location_on_land = factory.Faker('location_on_land')
        latitude = factory.LazyAttribute(lambda obj: obj.location_on_land[0])
        longitude = factory.LazyAttribute(lambda obj: obj.location_on_land[1])
        city_ = factory.LazyAttribute(lambda obj: obj.location_on_land[2])
        country_ = factory.LazyAttribute(lambda obj: obj.location_on_land[3])
        self_ = factory.LazyAttribute(lambda obj: obj)

    id = factory.Sequence(lambda n: n+1)
    address = ''
    city = factory.SelfAttribute('.city_')
    state = ''
    country = factory.SelfAttribute('.country_')
    postal_code = ''

    location = factory.RelatedFactoryList(
        LocationFactory,
        factory_related_name='address',
        size=1,
        address_id=factory.SelfAttribute('..id'),
        latitude=factory.SelfAttribute('..latitude'),
        longitude=factory.SelfAttribute('..longitude'),
    )

    customer_id = None
    customer = None
    warehouse_id = None
    warehouse = None


class CustomerFactory(TimestampedBaseFactory):
    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n+1)
    full_name = factory.Faker('name')

    address = factory.RelatedFactoryList(
        AddressFactory,
        factory_related_name='customer',
        size=1,
        customer_id=factory.SelfAttribute('..id'),
    )


class WarehouseFactory(TimestampedBaseFactory):
    class Meta:
        model = Warehouse

    id = factory.Sequence(lambda n: n+1)
    code = factory.Faker('hostname')

    address = factory.RelatedFactoryList(
        AddressFactory,
        factory_related_name='warehouse',
        size=1,
        warehouse_id=factory.SelfAttribute('..id'),
    )
