from sqlalchemy.orm import Session

from app.models.notification import Notification


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str
):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )

    db.add(notification)
    db.flush()

    return notification


def get_notifications_by_user(
    db: Session,
    user_id: int
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_notification_as_read(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
        .first()
    )

    if not notification:
        return None

    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return notification