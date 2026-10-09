from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.db.database import get_db
from app.models.user import User
from app.schemas.return_schema import ReturnCreate, ReturnResponse, ReturnStatusUpdate
from app.services.return_service import create_return, update_return_status


router = APIRouter(
    prefix="/returns",
    tags=["Returns"]
)


@router.post("/", response_model=ReturnResponse)
def create_return_request(
    request: ReturnCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_return(
            db=db,
            order_id=request.order_id,
            customer_id=current_user.id,
            reason=request.reason,
            items=request.items
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put("/{return_id}/status", response_model=ReturnResponse)
def update_status(
    return_id: int,
    request: ReturnStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("Admin")
    )
):
    try:
        return update_return_status(
            db=db,
            return_id=return_id,
            new_status=request.status,
            processed_by=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )