from sqlalchemy.orm import Session

from app.models.return_model import Return


def create_return(db: Session, return_request: Return):
    db.add(return_request)
    db.flush()
    return return_request


def get_return_by_id(db: Session, return_id: int):
    return (
        db.query(Return)
        .filter(Return.id == return_id)
        .first()
    )


def get_returns_by_order(db: Session, order_id: int):
    return (
        db.query(Return)
        .filter(Return.order_id == order_id)
        .order_by(Return.created_at.desc())
        .all()
    )


def update_return(db: Session, return_request: Return):
    db.commit()
    db.refresh(return_request)
    return return_request