from decimal import Decimal

from tests.factories import CustomerFactory, WarehouseFactory


DISTANCE_ENDPOINT = '/v2023.11.0/distance'


def test_calculate_distance(session, client, token):
    customer = CustomerFactory()
    warehouse = WarehouseFactory()

    session.add(customer)
    session.add(warehouse)
    session.commit()
    session.refresh(customer)
    session.refresh(warehouse)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert 'miles' in data
    assert 'kilometers' in data
    assert data['miles']
    assert data['kilometers']


def test_fail_to_calculate_distance_nonexistent_customer(session, client, token):
    warehouse = WarehouseFactory()

    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': 123,
            'warehouse_id': warehouse.id,
        },
    )
    data = response.json()

    assert response.status_code == 404
    assert response.json() == {'detail': 'Customer 123 not found.'}


def test_fail_to_calculate_distance_missing_customer_address(session, client, token):
    customer = CustomerFactory(address=None)
    warehouse = WarehouseFactory()

    session.add(customer)
    session.add(warehouse)
    session.commit()
    session.refresh(customer)
    session.refresh(warehouse)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
        },
    )
    data = response.json()

    assert response.status_code == 404
    assert response.json() == {'detail': f'Customer {customer.id} not found.'}


def test_fail_to_calculate_distance_missing_customer_address_location(session, client, token):
    customer = CustomerFactory(address__location=None)
    warehouse = WarehouseFactory()

    session.add(customer)
    session.add(warehouse)
    session.commit()
    session.refresh(customer)
    session.refresh(warehouse)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
        },
    )
    data = response.json()

    assert response.status_code == 404
    assert response.json() == {'detail': f'Customer {customer.id} not found.'}


def test_fail_to_calculate_distance_nonexistent_warehouse(session, client, token):
    customer = CustomerFactory()

    session.add(customer)
    session.commit()
    session.refresh(customer)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': 987,
        },
    )
    data = response.json()

    assert response.status_code == 404
    assert response.json() == {'detail': 'Warehouse 987 not found.'}


def test_fail_to_calculate_distance_missing_warehouse_address(session, client, token):
    customer = CustomerFactory()
    warehouse = WarehouseFactory(address=None)

    session.add(customer)
    session.add(warehouse)
    session.commit()
    session.refresh(customer)
    session.refresh(warehouse)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
        },
    )
    data = response.json()

    assert response.status_code == 404
    assert response.json() == {'detail': f'Warehouse {warehouse.id} not found.'}


def test_fail_to_calculate_distance_missing_warehouse_address_location(session, client, token):
    customer = CustomerFactory()
    warehouse = WarehouseFactory(address__location=None)

    session.add(customer)
    session.add(warehouse)
    session.commit()
    session.refresh(customer)
    session.refresh(warehouse)

    response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
        },
    )
    data = response.json()

    assert response.status_code == 404
    assert response.json() == {'detail': f'Warehouse {warehouse.id} not found.'}


def test_calculate_distance_method_query_parameter(session, client, token):
    customer = CustomerFactory()
    warehouse = WarehouseFactory()

    session.add(customer)
    session.add(warehouse)
    session.commit()
    session.refresh(customer)
    session.refresh(warehouse)

    default_response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
        },
    )
    default_data = default_response.json()
    assert default_response.status_code == 200

    geodesic_response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
            'method': 'geodesic',
        },
    )
    geodesic_data = geodesic_response.json()
    assert geodesic_response.status_code == 200

    great_circle_response = client.get(
        DISTANCE_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        params={
            'customer_id': customer.id,
            'warehouse_id': warehouse.id,
            'method': 'great-circle',
        },
    )
    great_circle_data = great_circle_response.json()
    assert great_circle_response.status_code == 200

    assert default_data == geodesic_data
    assert 0 < Decimal(geodesic_data['miles']) < Decimal(geodesic_data['kilometers'])
    assert 0 < Decimal(great_circle_data['miles']) < Decimal(great_circle_data['kilometers'])
