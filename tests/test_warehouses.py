
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


def test_create_warehouse():
    token = get_admin_token()

    response = client.post(
        "/warehouses/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Pytest Warehouse {uuid.uuid4().hex[:8]}",
            "location": "Hyderabad",
            "capacity": 1000
        }
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert "id" in data
    assert data["location"] == "Hyderabad"
    assert data["capacity"] == 1000
    assert data["is_active"] is True


def test_list_warehouses():
    token = get_admin_token()

    response = client.get(
        "/warehouses/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_get_warehouse():
    token = get_admin_token()

    response = client.get(
        "/warehouses/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == 1


def test_update_warehouse():
    token = get_admin_token()

    response = client.put(
        "/warehouses/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Warehouse",
            "location": "Hyderabad",
            "capacity": 2000
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Updated Warehouse"
    assert data["capacity"] == 2000


def test_deactivate_warehouse():
    token = get_admin_token()

    response = client.put(
        "/warehouses/1/deactivate",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == 1
    assert data["is_active"] is False


def test_activate_warehouse():
    token = get_admin_token()

    response = client.put(
        "/warehouses/1/activate",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == 1
    assert data["is_active"] is True


def test_customer_cannot_access_warehouses():
    token = get_customer_token()

    response = client.get(
        "/warehouses/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403, (
        f"Expected 403 Forbidden, got {response.status_code}: {response.text}"
    )
