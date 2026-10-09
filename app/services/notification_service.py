from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.repositories import notification_repository


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str
):
    return notification_repository.create_notification(
        db=db,
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )


def get_user_notifications(
    db: Session,
    user_id: int
):
    return notification_repository.get_notifications_by_user(
        db=db,
        user_id=user_id
    )


def mark_notification_read(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = notification_repository.mark_notification_as_read(
        db=db,
        notification_id=notification_id,
        user_id=user_id
    )

    if not notification:
        raise ValueError("Notification not found")

    return notification

def mark_all_notifications_read(
    db: Session,
    user_id: int
):
    notifications = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).all()

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return {
        "message": "All notifications marked as read",
        "updated_count": len(notifications)
    }