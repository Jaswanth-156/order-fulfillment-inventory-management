from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.repositories import audit_log_repository


def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    details: dict | None = None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )

    return audit_log_repository.create_audit_log(
        db=db,
        audit_log=audit_log
    )


def get_audit_logs(db: Session):
    return audit_log_repository.get_audit_logs(db)