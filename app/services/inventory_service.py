from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.repositories.inventory_repository import (
    get_inventory_by_product_and_warehouse,
    create_inventory,
    update_inventory,
)


def adjust_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    quantity: int,
    reason: str,
    user_id: int,
    reorder_level: int = 0
):
    if quantity == 0:
        raise ValueError("Quantity cannot be zero")

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise ValueError("Product not found")

    warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

    if not warehouse:
        raise ValueError("Warehouse not found")

    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).with_for_update().first()

    if not inventory:
        inventory = Inventory(
            product_id=product_id,
            warehouse_id=warehouse_id,
            available_quantity=0,
            reserved_quantity=0,
            damaged_quantity=0,
            reorder_level=reorder_level
        )

        db.add(inventory)
        db.flush()

    inventory.available_quantity += quantity

    if inventory.available_quantity < 0:
        raise ValueError("Insufficient inventory")

    if reorder_level is not None:
        inventory.reorder_level = reorder_level

    transaction = InventoryTransaction(
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type="ADJUSTMENT",
        quantity=quantity,
        reference_entity="inventory",
        reference_id=inventory.id,
        user_id=user_id,
        transaction_metadata={
            "reason": reason
        }
    )

    db.add(transaction)
    db.commit()
    db.refresh(inventory)

    return inventory

def reserve_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    quantity: int,
    user_id: int = None
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).with_for_update().first()

    if not inventory:
        raise ValueError("Inventory not found")

    if inventory.available_quantity < quantity:
        raise ValueError("Insufficient inventory")

    inventory.available_quantity -= quantity
    inventory.reserved_quantity += quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type="RESERVATION",
        quantity=quantity,
        user_id=user_id
    )

    db.add(transaction)

    db.flush()

    return inventory

def get_inventory(
    db: Session,
    warehouse_id: int = None,
    product_id: int = None,
    low_stock: bool = False,
    out_of_stock: bool = False,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Inventory)

    if warehouse_id is not None:
        query = query.filter(
            Inventory.warehouse_id == warehouse_id
        )

    if product_id is not None:
        query = query.filter(
            Inventory.product_id == product_id
        )

    if low_stock:
        query = query.filter(
            Inventory.available_quantity <= Inventory.reorder_level
        )

    if out_of_stock:
        query = query.filter(
            Inventory.available_quantity == 0
        )

    return query.offset(skip).limit(limit).all()


def get_low_stock_inventory(
    db: Session,
    warehouse_id: int = None
):
    query = db.query(Inventory).filter(
        Inventory.available_quantity <= Inventory.reorder_level
    )

    if warehouse_id is not None:
        query = query.filter(
            Inventory.warehouse_id == warehouse_id
        )

    return query.all()


def get_inventory_transactions(
    db: Session,
    product_id: int = None,
    warehouse_id: int = None
):
    query = db.query(InventoryTransaction)

    if product_id is not None:
        query = query.filter(
            InventoryTransaction.product_id == product_id
        )

    if warehouse_id is not None:
        query = query.filter(
            InventoryTransaction.warehouse_id == warehouse_id
        )

    return query.order_by(
        InventoryTransaction.created_at.desc()
    ).all()


def release_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    quantity: int,
    user_id: int = None
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id,
        Inventory.warehouse_id == warehouse_id
    ).with_for_update().first()

    if not inventory:
        raise ValueError("Inventory not found")

    if inventory.reserved_quantity < quantity:
        raise ValueError("Insufficient reserved inventory")

    inventory.reserved_quantity -= quantity
    inventory.available_quantity += quantity

    transaction = InventoryTransaction(
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type="RELEASE",
        quantity=quantity,
        user_id=user_id
    )

    db.add(transaction)
    db.flush()

    return inventory