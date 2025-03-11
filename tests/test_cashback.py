from http import HTTPStatus


def test_get_cashback(client, reseller, token, mocker):
    mock_data = {'statusCode': 200, 'body': {'credit': 100}}
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data
    mocker.patch('httpx.get', return_value=mock_response)

    response = client.get(
        '/cashback',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected = {
        'name': reseller.name,
        'cpf': reseller.cpf,
        'email': reseller.email,
        'credit': mock_data['body']['credit'],
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected


def test_get_cashback_error(client, reseller, token, mocker):
    mocker.patch('httpx.get', side_effect=Exception('Error'))

    response = client.get(
        '/cashback',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json()['detail'] == 'Unable to get cashback'
