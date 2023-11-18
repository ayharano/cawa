from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from cawa.settings import Settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

settings = Settings()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False


def create_access_token(data: dict[str, str | datetime]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt
