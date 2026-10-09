from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


def create_audit_log(db: Session, audit_log: AuditLog):
    db.add(audit_log)
    db.flush()
    return audit_log


def get_audit_logs(db: Session):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )