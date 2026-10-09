from sqlalchemy.orm import Session
from app.models.inventory import Inventory

def create_inventory(db:Session,inventory:Inventory):
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def get_inventory(
    db: Session,
    warehouse_id: int | None = None,
    product_id: int | None = None,
    low_stock: bool = False,
    out_of_stock: bool = False,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Inventory)

    if warehouse_id is not None:
        query = query.filter(Inventory.warehouse_id == warehouse_id)

    if product_id is not None:
        query = query.filter(Inventory.product_id == product_id)

    if low_stock:
        query = query.filter(
            Inventory.available_quantity <= Inventory.reorder_level
        )

    if out_of_stock:
        query = query.filter(
            Inventory.available_quantity == 0
        )

    return query.offset(skip).limit(limit).all()

def get_inventory_by_id(db:Session,inventory_id:int):
    return db.query(Inventory).filter(
        Inventory.id==inventory_id
    ).first()

def get_inventory_by_product_and_warehouse(
    db: Session,
    product_id: int,
    warehouse_id: int,
    for_update: bool = False
):
    query = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    )

    if for_update:
        query = query.with_for_update()

    return query.first()

def update_inventory(db:Session,inventory:Inventory):
    db.commit()
    db.refresh(inventory)
    return inventory

def get_low_stock_inventory(db: Session):
    return (
        db.query(Inventory)
        .filter(
            Inventory.available_quantity <= Inventory.reorder_level
        )
        .all()
    )