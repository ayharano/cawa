from datetime import datetime, timedelta

import time_machine

from cawa.security import settings


TOKEN_ENDPOINT = '/v2023.11.0/auth/token'
REFRESH_TOKEN_ENDPOINT = '/v2023.11.0/auth/refresh-token'


def test_get_token(client, user):
    response = client.post(
        TOKEN_ENDPOINT,
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_fail_to_get_token_nonexistent_user(client):
    response = client.post(
        TOKEN_ENDPOINT,
        data={
            'username': 'absent',
            'password': 'does not matter',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_fail_to_get_token_deactivated_user(client, user):
    user.is_active = False
    response = client.post(
        TOKEN_ENDPOINT,
        data={
            'username': user.username,
            'password': user.clean_password[:-1],
        },
    )
    token = response.json()

    assert response.status_code == 400
    assert response.json() == {'detail': 'User was deactivated'}


def test_fail_to_get_token_wrong_password(client, user):
    response = client.post(
        TOKEN_ENDPOINT,
        data={
            'username': user.username,
            'password': user.clean_password[:-1],
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        REFRESH_TOKEN_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert response.json()['token_type'] == 'bearer'


def test_fail_to_refresh_expired_token(client, user):
    response = client.post(
        TOKEN_ENDPOINT,
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )
    assert response.status_code == 200
    token = response.json()['access_token']

    after_first_token = datetime.utcnow()
    after_first_token_expiration = after_first_token + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        seconds=1.,
    )

    with time_machine.travel(after_first_token_expiration, tick=False):
        response = client.post(
            REFRESH_TOKEN_ENDPOINT,
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}
