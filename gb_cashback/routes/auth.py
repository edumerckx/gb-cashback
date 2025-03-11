from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.orm import Session as SessionORM

from gb_cashback.db import get_session
from gb_cashback.models import Reseller
from gb_cashback.schemas.auth import Token
from gb_cashback.security import (
    create_token,
    # get_current_reseller,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[SessionORM, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token, status_code=HTTPStatus.CREATED)
def login_for_access_token(form_data: OAuth2Form, session: Session):
    # conforme doc do fastapi, os dados para a autenticação vem como formulário
    # e tem os atributos 'username' e 'password'
    # https://fastapi.tiangolo.com/pt/tutorial/security/simple-oauth2/#pegue-o-username-nome-de-usuario-e-password-senha
    reseller = session.scalar(
        select(Reseller).where(or_(
            Reseller.cpf == form_data.username,
            Reseller.email == form_data.username
        ))
    )

    bad_request = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail='Invalid credentials'
    )

    if not reseller:
        raise bad_request

    if not verify_password(form_data.password, reseller.password):
        raise bad_request

    access_token = create_token(data={'sub': reseller.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
