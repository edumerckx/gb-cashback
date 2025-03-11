from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from gb_cashback.app import app
from gb_cashback.db import get_session
from gb_cashback.models import (
    Purchase,
    PurchaseStatus,
    Reseller,
    table_registry,
)
from gb_cashback.security import get_password_hash


@pytest.fixture
def client(session):
    def _get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = _get_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        poolclass=StaticPool,
        connect_args={'check_same_thread': False},
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def reseller(session):
    password = '123456'
    reseller = Reseller(
        name='Teste',
        cpf='12345678901',
        email='test@example.com',
        password=get_password_hash(password),
    )

    session.add(reseller)
    session.commit()
    session.refresh(reseller)

    reseller.raw_password = password

    return reseller


@pytest.fixture
def purchases(session, reseller):
    purchase_date = date(2022, 1, 1)
    purchase1 = Purchase(
        code='123',
        amount=1000,
        cpf=reseller.cpf,
        date=purchase_date,
        reseller_id=reseller.id,
        perc_cashback=10,
        cashback=100.0,
        status=PurchaseStatus.APPROVED,
    )

    purchase2 = Purchase(
        code='456',
        amount=2000,
        cpf=reseller.cpf,
        date=purchase_date,
        reseller_id=reseller.id,
        perc_cashback=20,
        cashback=400.0,
        status=PurchaseStatus.VALIDATION,
    )

    session.add_all([purchase1, purchase2])
    session.commit()


@pytest.fixture
def token(client, reseller):
    resp = client.post(
        '/auth/token',
        data={'username': reseller.email, 'password': reseller.raw_password},
    )
    return resp.json()['access_token']
