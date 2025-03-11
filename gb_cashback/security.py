from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session as SessionORM

from gb_cashback.db import get_session
from gb_cashback.models import Reseller
from gb_cashback.settings import Settings

pwd_context = PasswordHash.recommended()
settings = Settings()
OAuth2Scheme = Annotated[
    str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))
]
Session = Annotated[SessionORM, Depends(get_session)]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    return encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


def get_current_reseller(token: OAuth2Scheme, session: Session):
    exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Unable to validate credentials',
    )

    try:
        payload = decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        email = payload.get('sub')
        if not email:
            raise exception
    except DecodeError:
        raise exception
    except ExpiredSignatureError:
        raise exception

    reseller = session.scalar(select(Reseller).where(Reseller.email == email))

    if not reseller:
        raise exception

    return reseller
