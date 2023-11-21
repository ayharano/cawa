from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from cawa.models import User
from cawa.security import get_password_hash


def test_create_and_retrieve_user(session):
    before_new_user = datetime.utcnow()
    new_user = User(
        username='api-user',
        password=get_password_hash('VeryS@f&!'),
        is_active=True,
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(
        select(User)
        .where(User.username == 'api-user')
    )

    assert user.username == 'api-user'
    assert user.created > before_new_user
    assert user.updated > user.created


def test_cannot_create_duplicate_user(session):
    new_user = User(
        username='api-user',
        password=get_password_hash('VeryS@f&!'),
        is_active=True,
    )
    session.add(new_user)
    session.commit()

    new_user = User(
        username='api-user',
        password=get_password_hash('duplicate'),
        is_active=True,
    )
    session.add(new_user)
    with pytest.raises(IntegrityError):
        session.commit()
