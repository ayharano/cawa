from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from cawa.database import get_session
from cawa.models import User
from cawa.schemas import Token
from cawa.security import create_access_token, verify_password


router = APIRouter(prefix='/auth', tags=['token'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = session.scalar(
        select(User)
        .where(User.username == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password',
        )

    if not user.is_active:
        raise HTTPException(
            status_code=400, detail='User was deactivated',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
