from http import HTTPStatus


def test_create_token(client, reseller):
    data = {'username': reseller.email, 'password': reseller.raw_password}

    resp = client.post('/auth/token', data=data)
    token = resp.json()

    assert resp.status_code == HTTPStatus.CREATED
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'
