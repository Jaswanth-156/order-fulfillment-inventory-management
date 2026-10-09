from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import require_role
from app.db.database import get_db
from app.models.user import User
from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseResponse,
    WarehouseUpdate,
)
from app.services import warehouse_service


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


@router.post("/", response_model=WarehouseResponse, status_code=201)
def create_warehouse(
    warehouse_data: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return warehouse_service.create_warehouse(
        db=db,
        name=warehouse_data.name,
        location=warehouse_data.location,
        capacity=warehouse_data.capacity
    )


@router.get("/", response_model=list[WarehouseResponse])
def list_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return warehouse_service.get_warehouses(db)


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return warehouse_service.get_warehouse(
            db=db,
            warehouse_id=warehouse_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: int,
    warehouse_data: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return warehouse_service.update_warehouse(
            db=db,
            warehouse_id=warehouse_id,
            name=warehouse_data.name,
            location=warehouse_data.location,
            capacity=warehouse_data.capacity
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{warehouse_id}/activate", response_model=WarehouseResponse)
def activate_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return warehouse_service.activate_warehouse(
            db=db,
            warehouse_id=warehouse_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{warehouse_id}/deactivate", response_model=WarehouseResponse)
def deactivate_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return warehouse_service.deactivate_warehouse(
            db=db,
            warehouse_id=warehouse_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )