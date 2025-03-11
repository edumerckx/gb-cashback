from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SessionORM

from gb_cashback.calculator import cashback
from gb_cashback.db import get_session
from gb_cashback.models import Purchase, PurchaseStatus, Reseller
from gb_cashback.schemas.purchase import (
    PurchaseResponse,
    PurchaseResponseList,
    PurchaseSchema,
)
from gb_cashback.security import get_current_reseller
from gb_cashback.settings import Settings

router = APIRouter(prefix='/purchases', tags=['purchases'])
settings = Settings()

Session = Annotated[SessionORM, Depends(get_session)]
ResellerLogged = Annotated[Reseller, Depends(get_current_reseller)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=PurchaseResponse
)
def create_purchase(
    purchase: PurchaseSchema, session: Session, reseller: ResellerLogged
):
    value_cashback, perc_cashback = cashback(purchase.amount)
    new_purchase = Purchase(
        code=purchase.code,
        amount=purchase.amount,
        cpf=reseller.cpf,
        date=purchase.date,
        perc_cashback=perc_cashback,
        cashback=value_cashback,
        reseller_id=reseller.id,
    )

    resellers_with_purchase_approved = (
        settings.RESELLER_PURCHASE_APPROVED.split(',')
    )

    if reseller.cpf in resellers_with_purchase_approved:
        new_purchase.status = PurchaseStatus.APPROVED

    try:
        session.add(new_purchase)
        session.commit()
        session.refresh(new_purchase)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'Purchase (code {purchase.code}) already exists',
        )

    return new_purchase


@router.get('/', status_code=HTTPStatus.OK, response_model=PurchaseResponseList)
def get_purchases(session: Session, reseller: ResellerLogged):
    purchases = session.scalars(
        select(Purchase).where(Purchase.reseller_id == reseller.id)
    ).all()
    return {'purchases': purchases}
