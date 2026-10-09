
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

    assert response.status_code == 200, (
        f"Admin login failed: {response.status_code} - {response.text}"
    )

    return response.json()["access_token"]


def get_customer_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123456"
        }
    )

    assert response.status_code == 200, (
        f"Customer login failed: {response.status_code} - {response.text}"
    )

    return response.json()["access_token"]


def test_create_return():
    token = get_admin_token()

    response = client.post(
        "/returns/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "order_id": 3,
            "reason": "Product damaged",
            "items": [
                {
                    "product_id": 2,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["order_id"] == 3
    assert data["customer_id"] == 1
    assert data["status"] == "Requested"
    assert len(data["items"]) == 1


def test_admin_can_update_return_status():
    token = get_admin_token()

    create_response = client.post(
        "/returns/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "order_id": 3,
            "reason": "Testing return workflow",
            "items": [
                {
                    "product_id": 2,
                    "quantity": 1
                }
            ]
        }
    )

    assert create_response.status_code == 200, create_response.text

    return_id = create_response.json()["id"]

    response = client.put(
        f"/returns/{return_id}/status",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "status": "Approved"
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == return_id
    assert data["status"] == "Approved"


def test_customer_cannot_update_return_status():
    customer_token = get_customer_token()

    response = client.put(
        "/returns/999/status",
        headers={
            "Authorization": f"Bearer {customer_token}"
        },
        json={
            "status": "Approved"
        }
    )

    assert response.status_code == 403, (
        f"Expected 403 Forbidden, got {response.status_code}: {response.text}"
    )