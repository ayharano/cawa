TOKEN_ENDPOINT = '/v2023.11.0/auth/token'


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
