
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


def test_create_product():
    access_token = get_admin_token()

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "sku": f"TEST-SKU-{uuid.uuid4().hex[:8]}",
            "name": "Test Product",
            "description": "Product created by pytest",
            "category_id": 1,
            "price": 100,
            "cost_price": 70
        }
    )

    assert response.status_code == 201, (
        f"Product creation failed: {response.status_code} - {response.text}"
    )

    data = response.json()

    assert data["name"] == "Test Product"
    assert data["category_id"] == 1
    assert data["is_active"] is True


def test_customer_cannot_create_product():
    access_token = get_customer_token()

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "sku": f"TEST-CUSTOMER-{uuid.uuid4().hex[:8]}",
            "name": "Unauthorized Product",
            "description": "Should not be created",
            "category_id": 1,
            "price": 100,
            "cost_price": 70
        }
    )

    assert response.status_code == 403, (
        f"Expected 403 Forbidden, got {response.status_code}: {response.text}"
    )