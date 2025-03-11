from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class PurchaseStatus(str, Enum):
    VALIDATION = 'Em validação'
    APPROVED = 'Aprovado'


@table_registry.mapped_as_dataclass
class Reseller:
    __tablename__ = 'resellers'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    cpf: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
    purchases: Mapped[list['Purchase']] = relationship(
        back_populates='reseller', init=False
    )


@table_registry.mapped_as_dataclass
class Purchase:
    __tablename__ = 'purchases'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    code: Mapped[str] = mapped_column(unique=True)
    amount: Mapped[float]
    cpf: Mapped[str]
    date: Mapped[datetime]
    perc_cashback: Mapped[float]
    cashback: Mapped[float]
    reseller_id: Mapped[int] = mapped_column(ForeignKey('resellers.id'))
    status: Mapped[PurchaseStatus] = mapped_column(
        default=PurchaseStatus.VALIDATION
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
    reseller: Mapped[Reseller] = relationship(
        back_populates='purchases', init=False
    )
