CUSTOMERS_ENDPOINT = '/v2023.11.0/customers'


def test_create_customer(client, token):
    response = client.post(
        CUSTOMERS_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json={
            'full_name': '\t\f\v John Doe\r\n ',
            'address': '  760 United Nations Plaza\t\n',
            'city': '\tNew York City\n',
            'state': ' NY ',
            'country': '\r\nUSA\r\n',
            'postal_code': '10017',
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert data == {
        'full_name': 'John Doe',
        'address': '760 United Nations Plaza',
        'city': 'New York City',
        'state': 'NY',
        'country': 'USA',
        'postal_code': '10017',
        'id': 1,
    }
