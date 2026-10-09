from fastapi import APIRouter,Depends,HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_role
from app.db.database import get_db
from app.models.user import User
from app.schemas.inventory import(
    InventoryAdjustRequest,
    InventoryReleaseRequest,
    InventoryReserveRequest,
    InventoryResponse,
    InventoryTransferRequest
)
from app.schemas.inventory_transaction import InventoryTransactionResponse
from app.services import inventory_service

router=APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("/", response_model=list[InventoryResponse])
def list_inventory(
    warehouse_id: int | None = None,
    product_id: int | None = None,
    low_stock: bool = False,
    out_of_stock: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return inventory_service.get_inventory(
        db=db,
        warehouse_id=warehouse_id,
        product_id=product_id,
        low_stock=low_stock,
        out_of_stock=out_of_stock,
        skip=skip,
        limit=limit
    )

@router.post("/adjust", response_model=InventoryResponse)
def adjust_inventory(
    inventory_data: InventoryAdjustRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return inventory_service.adjust_inventory(
            db=db,
            product_id=inventory_data.product_id,
            warehouse_id=inventory_data.warehouse_id,
            quantity=inventory_data.quantity,
            reason=inventory_data.reason,
            user_id=current_user.id,
            reorder_level=inventory_data.reorder_level
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/transfer")
def transfer_inventory(
    inventory_data: InventoryTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        source_inventory, destination_inventory = (
            inventory_service.transfer_inventory(
                db=db,
                product_id=inventory_data.product_id,
                from_warehouse_id=inventory_data.from_warehouse_id,
                to_warehouse_id=inventory_data.to_warehouse_id,
                quantity=inventory_data.quantity,
                user_id=current_user.id
            )
        )

        return {
            "message": "Inventory transferred successfully",
            "source_inventory": source_inventory,
            "destination_inventory": destination_inventory
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get("/transactions",response_model=list[InventoryTransactionResponse])
def list_inventory_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return inventory_service.get_inventory_transactions(db)

@router.get("/low-stock", response_model=list[InventoryResponse])
def list_low_stock_inventory(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return inventory_service.get_low_stock_inventory(db)

@router.get("/{inventory_id}",response_model=InventoryResponse)
def get_inventory(
    inventory_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(require_role("Admin"))
):
    try:
        return inventory_service.get_inventory_by_id(
            db=db,
            inventory_id=inventory_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )



@router.post("/reserve", response_model=InventoryResponse)
def reserve_inventory(
    inventory_data: InventoryReserveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return inventory_service.reserve_inventory(
            db=db,
            product_id=inventory_data.product_id,
            warehouse_id=inventory_data.warehouse_id,
            quantity=inventory_data.quantity,
            user_id=current_user.id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.post("/release", response_model=InventoryResponse)
def release_inventory(
    inventory_data: InventoryReleaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return inventory_service.release_inventory(
            db=db,
            product_id=inventory_data.product_id,
            warehouse_id=inventory_data.warehouse_id,
            quantity=inventory_data.quantity,
            user_id=current_user.id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

