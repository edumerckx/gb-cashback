from pydantic import BaseModel


class CashbackResponse(BaseModel):
    name: str
    cpf: str
    email: str
    credit: float
