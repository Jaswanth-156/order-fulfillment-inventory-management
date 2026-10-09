from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import require_role
from app.db.database import get_db
from app.models.user import User
from app.services.audit_log_service import get_audit_logs

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("/")
def get_all_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return get_audit_logs(db)