from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.models.order import Order


client = TestClient(app)


def get_customer_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123456"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_idempotency_prevents_duplicate_order():
    token = get_customer_token()

    idempotency_key = "pytest-idempotency-unique-001"

    order_data = {
        "warehouse_id": 1,
        "items": [
            {
                "product_id": 2,
                "quantity": 1
            }
        ]
    }

    first_response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": idempotency_key
        },
        json=order_data
    )

    assert first_response.status_code == 200

    first_order = first_response.json()

    db = SessionLocal()

    count_before = db.query(Order).count()

    db.close()

    second_response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": idempotency_key
        },
        json=order_data
    )

    assert second_response.status_code == 200

    second_order = second_response.json()

    db = SessionLocal()

    count_after = db.query(Order).count()

    db.close()

    assert first_order["id"] == second_order["id"]
    assert first_order["order_number"] == second_order["order_number"]
    assert count_after == count_before

def test_same_idempotency_key_with_different_request():
    token = get_customer_token()

    key = "pytest-idempotency-different-request-001"

    first_order = {
        "warehouse_id": 1,
        "items": [
            {
                "product_id": 2,
                "quantity": 1
            }
        ]
    }

    second_order = {
        "warehouse_id": 1,
        "items": [
            {
                "product_id": 2,
                "quantity": 2
            }
        ]
    }

    first_response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": key
        },
        json=first_order
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": key
        },
        json=second_order
    )

    assert second_response.status_code in [400, 409]