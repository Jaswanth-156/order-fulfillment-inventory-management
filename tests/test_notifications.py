
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


def test_customer_can_get_notifications():
    token = get_customer_token()

    response = client.get(
        "/notifications/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_admin_can_get_notifications():
    token = get_admin_token()

    response = client.get(
        "/notifications/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_mark_notification_as_read():
    token = get_admin_token()

    notifications_response = client.get(
        "/notifications/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert notifications_response.status_code == 200, (
        notifications_response.text
    )

    notifications = notifications_response.json()

    if not notifications:
        return

    notification_id = notifications[0]["id"]

    response = client.put(
        f"/notifications/{notification_id}/read",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == notification_id
    assert data["is_read"] is True


def test_user_cannot_mark_another_users_notification_as_read():
    customer_token = get_customer_token()

    response = client.put(
        "/notifications/5/read",
        headers={
            "Authorization": f"Bearer {customer_token}"
        }
    )

    # The endpoint should not allow a user to read another user's notification.
    assert response.status_code in (403, 404), response.text
