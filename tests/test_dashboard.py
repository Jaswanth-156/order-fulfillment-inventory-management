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


def test_admin_can_access_dashboard():
    token = get_admin_token()

    response = client.get(
        "/dashboard/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_orders" in data
    assert "pending_orders" in data
    assert "processing_orders" in data
    assert "shipped_orders" in data
    assert "delivered_orders" in data
    assert "cancelled_orders" in data
    assert "total_products" in data
    assert "low_stock_items" in data
    assert "total_warehouses" in data


def test_customer_cannot_access_dashboard():
    token = get_customer_token()

    response = client.get(
        "/dashboard/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403