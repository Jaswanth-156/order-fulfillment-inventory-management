
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


def test_admin_can_assign_order():
    token = get_admin_token()

    response = client.post(
        "/order-assignments/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "order_id": 8,
            "agent_id": 2
        }
    )

    assert response.status_code == 200, (
        f"Order assignment failed: {response.status_code} - {response.text}"
    )

    data = response.json()

    assert data["order_id"] == 8
    assert data["agent_id"] == 2


def test_customer_cannot_assign_order():
    token = get_customer_token()

    response = client.post(
        "/order-assignments/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "order_id": 8,
            "agent_id": 2
        }
    )

    assert response.status_code == 403, (
        f"Expected 403 Forbidden, got {response.status_code}: {response.text}"
    )
