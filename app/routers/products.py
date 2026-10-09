from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import require_role
from app.db.database import get_db
from app.models.user import User
from app.schemas.product import (ProductCreate, ProductResponse,ProductUpdate,)
from app.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse,status_code=201)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return product_service.create_product(
            db=db,
            sku=product_data.sku,
            name=product_data.name,
            description=product_data.description,
            category_id=product_data.category_id,
            price=product_data.price,
            cost_price=product_data.cost_price,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get("/",response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    return product_service.get_products(db)


@router.get("/{product_id}",response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return product_service.get_product(
            db=db,
            product_id=product_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{product_id}",response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return product_service.update_product(
            db=db,
            product_id=product_id,
            name=product_data.name,
            description=product_data.description,
            category_id=product_data.category_id,
            price=product_data.price,
            cost_price=product_data.cost_price,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{product_id}/activate",response_model=ProductResponse)
def activate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return product_service.activate_product(
            db=db,
            product_id=product_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put("/{product_id}/deactivate",response_model=ProductResponse)
def deactivate_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin"))
):
    try:
        return product_service.deactivate_product(
            db=db,
            product_id=product_id
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )