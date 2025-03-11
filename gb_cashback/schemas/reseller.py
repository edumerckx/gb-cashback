from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class ResellerSchema(BaseModel):
    name: str
    cpf: str = Field(min_length=11, max_length=11, pattern=r'^\d{11}$')
    email: EmailStr
    password: str


class ResellerResponse(BaseModel):
    id: int
    name: str
    cpf: str
    email: EmailStr
