from fastapi import Header, HTTPException


def get_idempotency_key(
    idempotency_key: str | None = Header(default=None)
):
    if not idempotency_key:
        raise HTTPException(
            status_code=400,
            detail="Idempotency-Key header is required"
        )

    return idempotency_key