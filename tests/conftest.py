import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from cawa.database import get_session
from cawa.main import app
from cawa.models import Base
from cawa.routers import CURRENT_TOKEN_URL
from cawa.security import get_password_hash
from tests.factories import UserFactory


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    password = 'not very safe plain text password'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    # Python allows assigning new attributes, so we use this for password testing
    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        CURRENT_TOKEN_URL,
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )
    return response.json()['access_token']
