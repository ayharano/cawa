from datetime import datetime, timedelta

import factory

from cawa.models import User


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
