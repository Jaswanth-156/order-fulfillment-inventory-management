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


def test_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Admin@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    token = get_admin_token()

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "admin@gmail.com"
    assert data["role"] == "Admin"
    assert data["is_active"] is True


def test_refresh_token():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Admin@12345"
        }
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/auth/refresh",
        params={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_logout():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Admin@12345"
        }
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/auth/logout",
        params={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"


def test_inactive_user_cannot_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "Inactive@123456"
        }
    )

    assert response.status_code in [401, 403]


def test_customer_cannot_access_admin_dashboard():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123456"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.get(
        "/dashboard/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_change_password():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123456"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "Test@123456",
            "new_password": "Test@123457"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"

    # Login with the new password
    login_response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123457"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Change the password back to the original test password
    response = client.post(
        "/auth/change-password",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "current_password": "Test@123457",
            "new_password": "Test@123456"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"