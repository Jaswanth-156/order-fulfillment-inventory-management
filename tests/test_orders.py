from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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


def create_test_order(token):
    response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": f"pytest-order-{uuid4()}"
        },
        json={
            "warehouse_id": 1,
            "items": [
                {
                    "product_id": 2,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 200, (
        f"Order creation failed: {response.status_code} - {response.text}"
    )

    return response.json()


def test_create_order():
    token = get_customer_token()

    response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": "pytest-order-001"
        },
        json={
            "warehouse_id": 1,
            "items": [
                {
                    "product_id": 2,
                    "quantity": 1
                }
            ]
        }
    )

    assert response.status_code == 200, (
        f"Order creation failed: {response.status_code} - {response.text}"
    )

    data = response.json()

    assert "id" in data
    assert "order_number" in data
    assert data["customer_id"] == 4


def test_create_order_same_idempotency_key():
    token = get_customer_token()

    payload = {
        "warehouse_id": 1,
        "items": [
            {
                "product_id": 2,
                "quantity": 1
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Idempotency-Key": "pytest-order-002"
    }

    response1 = client.post(
        "/orders/",
        headers=headers,
        json=payload
    )

    assert response1.status_code == 200, (
        f"First order request failed: "
        f"{response1.status_code} - {response1.text}"
    )

    response2 = client.post(
        "/orders/",
        headers=headers,
        json=payload
    )

    assert response2.status_code == 200, (
        f"Repeated order request failed: "
        f"{response2.status_code} - {response2.text}"
    )

    data1 = response1.json()
    data2 = response2.json()

    assert data1["id"] == data2["id"]
    assert data1["order_number"] == data2["order_number"]


def test_order_status_history():
    token = get_customer_token()
    order = create_test_order(token)

    response = client.get(
        f"/orders/{order['id']}/status-history",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200, (
        f"Status history request failed: "
        f"{response.status_code} - {response.text}"
    )

    assert isinstance(response.json(), list)


def test_update_order_status():
    customer_token = get_customer_token()
    admin_token = get_admin_token()

    order = create_test_order(customer_token)

    response = client.put(
        f"/orders/{order['id']}/status",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "status": "CONFIRMED"
        }
    )

    assert response.status_code == 200, (
        f"Status update failed: {response.status_code} - {response.text}"
    )

    data = response.json()

    assert data["id"] == order["id"]
    assert data["status"] == "CONFIRMED"


def test_cancel_order():
    customer_token = get_customer_token()
    order = create_test_order(customer_token)

    response = client.put(
        f"/orders/{order['id']}/cancel",
        headers={
            "Authorization": f"Bearer {customer_token}"
        }
    )

    assert response.status_code == 200, (
        f"Order cancellation failed: "
        f"{response.status_code} - {response.text}"
    )

    data = response.json()

    assert data["id"] == order["id"]
    assert data["status"] == "CANCELLED"