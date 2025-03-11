from datetime import date

from pydantic import BaseModel, Field

from gb_cashback.models import PurchaseStatus


class PurchaseSchema(BaseModel):
    code: str
    amount: float = Field(gt=0)
    date: date


class PurchaseResponse(BaseModel):
    id: int
    code: str
    amount: float
    cpf: str
    date: date
    perc_cashback: float
    cashback: float
    status: PurchaseStatus


class PurchaseResponseList(BaseModel):
    purchases: list[PurchaseResponse]
