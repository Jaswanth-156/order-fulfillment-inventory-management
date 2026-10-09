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


def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401