from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.inventory_transfer import (
    InventoryTransferCreate,
    InventoryTransferResponse
)
from app.services.inventory_transfer_service import transfer_inventory

router = APIRouter(
    prefix="/inventory-transfers",
    tags=["Inventory Transfers"]
)

@router.post("/",response_model=InventoryTransferResponse)
def create_inventory_transfer(
    request: InventoryTransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return transfer_inventory(
            db=db,
            product_id=request.product_id,
            from_warehouse_id=request.from_warehouse_id,
            to_warehouse_id=request.to_warehouse_id,
            quantity=request.quantity,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )