from sqlalchemy.orm import Session

from app.models.order import Order


def create_order(db: Session, order: Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def get_order_by_number(db: Session, order_number: str):
    return (
        db.query(Order)
        .filter(Order.order_number == order_number)
        .first()
    )