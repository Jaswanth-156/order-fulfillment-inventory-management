from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.idempotency import get_idempotency_key
from app.db.database import get_db
from app.models.user import User
from app.repositories.order_status_history_repository import get_history_by_order
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.schemas.order_status_history import OrderStatusHistoryResponse
from app.services.order_service import cancel_order, create_order, update_order_status


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_new_order(
    request: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str = Depends(get_idempotency_key)
):
    try:
        return create_order(
            db=db,
            customer_id=current_user.id,
            warehouse_id=request.warehouse_id,
            items=request.items,
            expected_delivery_date=request.expected_delivery_date,
            idempotency_key=idempotency_key
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.put("/{order_id}/status",response_model=OrderResponse)
def update_status(
    order_id: int,
    request: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_order_status(
        db=db,
        order_id=order_id,
        new_status=request.status,
        changed_by=current_user.id
    )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/{order_id}/status-history",response_model=list[OrderStatusHistoryResponse])
def get_order_status_history(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_history_by_order(
        db=db,
        order_id=order_id
    )

@router.put("/{order_id}/cancel",response_model=OrderResponse)
def cancel_existing_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return cancel_order(
            db=db,
            order_id=order_id,
            cancelled_by=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )