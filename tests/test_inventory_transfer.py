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


def test_inventory_transfer():
    token = get_admin_token()

    response = client.post(
        "/inventory-transfers/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_id": 2,
            "from_warehouse_id": 1,
            "to_warehouse_id": 2,
            "quantity": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 2
    assert data["from_warehouse_id"] == 1
    assert data["to_warehouse_id"] == 2
    assert data["quantity"] == 1


def test_inventory_transfer_same_warehouse():
    token = get_admin_token()

    response = client.post(
        "/inventory-transfers/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_id": 2,
            "from_warehouse_id": 1,
            "to_warehouse_id": 1,
            "quantity": 1
        }
    )

    assert response.status_code == 400


def test_inventory_transfer_invalid_quantity():
    token = get_admin_token()

    response = client.post(
        "/inventory-transfers/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "product_id": 2,
            "from_warehouse_id": 1,
            "to_warehouse_id": 2,
            "quantity": 0
        }
    )

    assert response.status_code == 422