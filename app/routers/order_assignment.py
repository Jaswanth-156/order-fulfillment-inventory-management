from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.order_assignment import (
    OrderAssignmentCreate,
    OrderAssignmentResponse
)
from app.services.order_assignment_service import assign_order
from app.core.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/order-assignments",
    tags=["Order Assignments"]
)

@router.post("/",response_model=OrderAssignmentResponse)
def assign_order_to_agent(
    request: OrderAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:

        return assign_order(
            db=db,
            order_id=request.order_id,
            agent_id=request.agent_id,
            assigned_by=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))