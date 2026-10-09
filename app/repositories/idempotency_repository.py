from sqlalchemy.orm import Session

from app.models.idempotency_key import IdempotencyKey


def get_by_key(db: Session, key: str):
    return (
        db.query(IdempotencyKey)
        .filter(IdempotencyKey.key == key)
        .first()
    )


def create_idempotency_key(
    db: Session,
    idempotency_key: IdempotencyKey
):
    db.add(idempotency_key)
    db.flush()
    return idempotency_key


def update_response(
    db: Session,
    idempotency_key: IdempotencyKey,
    response_status: int,
    response_body: str
):
    idempotency_key.response_status = response_status
    idempotency_key.response_body = response_body
    db.flush()

    return idempotency_key