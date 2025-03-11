from http import HTTPStatus


def test_create_reseller(client):
    response = client.post(
        '/resellers',
        json={
            'name': 'Teste',
            'cpf': '12345678901',
            'email': 'test@example.com',
            'password': '123456',
        },
    )

    expected = {
        'id': 1,
        'name': 'Teste',
        'cpf': '12345678901',
        'email': 'test@example.com',
    }

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected


def test_reseller_already_exists(client, reseller):
    response = client.post(
        '/resellers',
        json={
            'name': 'Teste',
            'cpf': reseller.cpf,
            'email': reseller.email,
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Reseller already exists'
