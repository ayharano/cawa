WAREHOUSES_ENDPOINT = '/v2023.11.0/warehouses'


def test_create_warehouse(client, token):
    response = client.post(
        WAREHOUSES_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json={
            'code': '\t\f\v port-usa-ca-losangeles\r\n ',
            'address': '  Port of Los Angeles\t\n',
            'city': '\nLos Angeles\t',
            'state': '  CA ',
            'country': '\r\nUSA\r\n',
            'postal_code': '\t \n',
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert data == {
        'code': 'port-usa-ca-losangeles',
        'address': 'Port of Los Angeles',
        'city': 'Los Angeles',
        'state': 'CA',
        'country': 'USA',
        'postal_code': '',
        'id': 1,
    }
