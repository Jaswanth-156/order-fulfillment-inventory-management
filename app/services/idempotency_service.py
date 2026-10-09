from sqlalchemy.orm import Session

from app.models.idempotency_key import IdempotencyKey
from app.repositories import idempotency_repository


def get_existing_key(db: Session, key: str):
    return idempotency_repository.get_by_key(db, key)


def create_key(
    db: Session,
    key: str,
    user_id: int,
    request_hash: str
):
    idempotency_key = IdempotencyKey(
        key=key,
        user_id=user_id,
        request_hash=request_hash
    )

    return idempotency_repository.create_idempotency_key(
        db=db,
        idempotency_key=idempotency_key
    )


def save_response(
    db: Session,
    idempotency_key: IdempotencyKey,
    response_status: int,
    response_body: str
):
    return idempotency_repository.update_response(
        db=db,
        idempotency_key=idempotency_key,
        response_status=response_status,
        response_body=response_body
    )