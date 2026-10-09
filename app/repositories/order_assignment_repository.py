from sqlalchemy.orm import Session

from app.models.order_assignment import OrderAssignment


def create_assignment(db: Session, assignment: OrderAssignment):
    db.add(assignment)
    db.flush()
    return assignment


def get_assignment_by_order(db: Session, order_id: int):
    return (
        db.query(OrderAssignment)
        .filter(OrderAssignment.order_id == order_id)
        .order_by(OrderAssignment.assigned_at.desc())
        .first()
    )


def get_assignments_by_order(db: Session, order_id: int):
    return (
        db.query(OrderAssignment)
        .filter(OrderAssignment.order_id == order_id)
        .order_by(OrderAssignment.assigned_at.desc())
        .all()
    )