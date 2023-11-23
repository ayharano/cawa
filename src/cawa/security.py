from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from sqlalchemy import select
from sqlalchemy.orm import Session

from cawa.database import get_session
from cawa.models import User
from cawa.routers import CURRENT_TOKEN_URL
from cawa.schemas import TokenData
from cawa.settings import Settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=CURRENT_TOKEN_URL[1:])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

settings = Settings()


CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


DeactivatedUserException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='User was deactivated',
    headers={'WWW-Authenticate': 'Bearer'},
)


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


def get_current_active_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise CredentialsException

    username: str = payload.get('sub')
    if not username:
        raise CredentialsException
    token_data = TokenData(username=username)

    user = session.scalar(
        select(User)
        .where(User.username == token_data.username)
    )

    if user is None:
        raise CredentialsException

    if not user.is_active:
        raise DeactivatedUserException

    return user
