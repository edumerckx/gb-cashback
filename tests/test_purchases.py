from http import HTTPStatus

from gb_cashback.models import PurchaseStatus


def test_create_purchase(client, reseller, token):
    response = client.post(
        '/purchases',
        json={
            'code': '123456',
            'amount': 100,
            'cpf': reseller.cpf,
            'date': '2022-01-01',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    expected = {
        'id': 1,
        'code': '123456',
        'amount': 100,
        'cpf': reseller.cpf,
        'date': '2022-01-01',
        'perc_cashback': 10,
        'cashback': 10.0,
        'status': PurchaseStatus.VALIDATION,
    }
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected


def test_create_purchase_approved(client):
    response_reseller = client.post(
        '/resellers',
        json={
            'name': 'Teste',
            'cpf': '15350946056',
            'email': 'test@example.com',
            'password': '123456',
        },
    )
    reseller = response_reseller.json()

    data = {'username': '15350946056', 'password': '123456'}
    response_auth = client.post('/auth/token', data=data)
    token = response_auth.json()['access_token']

    response = client.post(
        '/purchases',
        json={
            'code': '123456',
            'amount': 100,
            'cpf': reseller['cpf'],
            'date': '2022-01-01',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    expected = {
        'id': 1,
        'code': '123456',
        'amount': 100,
        'cpf': reseller['cpf'],
        'date': '2022-01-01',
        'perc_cashback': 10,
        'cashback': 10.0,
        'status': PurchaseStatus.APPROVED,
    }
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected


def test_list_purchases(client, token, purchases):
    response = client.get(
        '/purchases',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()
    expected_len = 2

    assert response.status_code == HTTPStatus.OK
    assert 'purchases' in data
    assert len(response.json()['purchases']) == expected_len


def test_list_purchases_empty(client, token):
    response = client.get(
        '/purchases',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()
    expected = []

    assert response.status_code == HTTPStatus.OK
    assert 'purchases' in data
    assert data['purchases'] == expected
