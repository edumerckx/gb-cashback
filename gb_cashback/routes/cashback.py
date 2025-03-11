from http import HTTPStatus
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as SessionORM

from gb_cashback.db import get_session
from gb_cashback.models import Reseller
from gb_cashback.schemas.cashback import CashbackResponse
from gb_cashback.security import get_current_reseller
from gb_cashback.settings import Settings

router = APIRouter(prefix='/cashback', tags=['cashback'])

settings = Settings()

Session = Annotated[SessionORM, Depends(get_session)]
ResellerLogged = Annotated[Reseller, Depends(get_current_reseller)]


@router.get('/', status_code=HTTPStatus.OK, response_model=CashbackResponse)
def get_cashback(reseller: ResellerLogged):
    try:
        response = httpx.get(
            f'{settings.CASHBACK_EXTERNAL_URL}{reseller.cpf}',
            headers={'token': settings.CASHBACK_EXTERNAL_TOKEN},
        )
        data = response.json()['body']
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Unable to get cashback',)

    return {
        'name': reseller.name,
        'cpf': reseller.cpf,
        'email': reseller.email,
        'credit': data['credit'],
    }
