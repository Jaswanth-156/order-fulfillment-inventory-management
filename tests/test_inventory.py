import uuid

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_admin_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Admin@12345"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_list_inventory():
    token = get_admin_token()

    response = client.get(
        "/inventory/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_low_stock_inventory():
    token = get_admin_token()

    response = client.get(
        "/inventory/low-stock",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_inventory_transactions():
    token = get_admin_token()

    response = client.get(
        "/inventory/transactions",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_customer_cannot_access_inventory():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123456"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/inventory/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_adjust_inventory():
    token = get_admin_token()

    response = client.post(
        "/inventory/adjust",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_id": 2,
            "warehouse_id": 1,
            "quantity": 5,
            "reason": "Pytest inventory adjustment",
            "reorder_level": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 2
    assert data["warehouse_id"] == 1
    assert data["available_quantity"] >= 0


def test_reserve_inventory():
    token = get_admin_token()

    response = client.post(
        "/inventory/reserve",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_id": 2,
            "warehouse_id": 1,
            "quantity": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 2
    assert data["warehouse_id"] == 1
    assert data["reserved_quantity"] >= 1


def test_release_inventory():
    token = get_admin_token()

    response = client.post(
        "/inventory/release",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_id": 2,
            "warehouse_id": 1,
            "quantity": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 2
    assert data["warehouse_id"] == 1