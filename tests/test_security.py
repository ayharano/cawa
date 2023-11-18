from datetime import datetime, timedelta

from jose import jwt

from cawa.security import create_access_token, settings


def test_jwt():
    data = {'key': 'value'}
    before = datetime.now()
    before_plus_expire_minutes = (
        before + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    ).replace(microsecond=0)

    token = create_access_token(data)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['key'] == data['key']
    assert decoded['exp']
    exp_timestamp = datetime.fromtimestamp(decoded['exp'])
    assert before_plus_expire_minutes <= exp_timestamp
