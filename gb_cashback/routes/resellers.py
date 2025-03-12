from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionORM

from gb_cashback.db import get_session
from gb_cashback.logger import get_logger
from gb_cashback.models import Reseller
from gb_cashback.schemas.reseller import ResellerResponse, ResellerSchema
from gb_cashback.security import get_password_hash
from gb_cashback.settings import Settings

router = APIRouter(prefix='/resellers', tags=['resellers'])

Session = Annotated[SessionORM, Depends(get_session)]
logger = get_logger(Settings().LOGGER_LEVEL)

@router.post(
    '/', response_model=ResellerResponse, status_code=HTTPStatus.CREATED
)
def create_reseller(reseller: ResellerSchema, session: Session):
    new_reseller = Reseller(
        name=reseller.name,
        cpf=reseller.cpf,
        email=reseller.email,
        password=get_password_hash(reseller.password),
    )

    try:
        session.add(new_reseller)
        session.commit()
        session.refresh(new_reseller)

        logger.info(f'Reseller (cpf {reseller.cpf}) created')
        return new_reseller
    except IntegrityError:
        logger.error(f'Reseller (cpf {reseller.cpf}) already exists')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Reseller already exists',
        )
