from sqlalchemy.orm import Session

from app.models.order_status_history import OrderStatusHistory


def get_history_by_order(db: Session, order_id: int):
    return (
        db.query(OrderStatusHistory)
        .filter(OrderStatusHistory.order_id == order_id)
        .order_by(OrderStatusHistory.created_at.asc())
        .all()
    )