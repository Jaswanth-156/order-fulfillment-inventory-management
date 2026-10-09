from sqlalchemy.orm import Session

from app.models.inventory_transaction import InventoryTransaction
from app.repositories.inventory_transfer_repository import get_inventory


def transfer_inventory(
    db: Session,
    product_id: int,
    from_warehouse_id: int,
    to_warehouse_id: int,
    quantity: int,
    user_id: int
):
    if from_warehouse_id == to_warehouse_id:
        raise ValueError("Source and destination warehouses must be different")

    if quantity <= 0:
        raise ValueError("Transfer quantity must be greater than zero")

    source_inventory = get_inventory(
        db,
        product_id,
        from_warehouse_id
    )

    destination_inventory = get_inventory(
        db,
        product_id,
        to_warehouse_id
    )

    if not source_inventory:
        raise ValueError("Source inventory not found")

    if not destination_inventory:
        raise ValueError("Destination inventory not found")

    if source_inventory.available_quantity < quantity:
        raise ValueError("Insufficient inventory")

    source_inventory.available_quantity -= quantity
    destination_inventory.available_quantity += quantity

    source_transaction = InventoryTransaction(
        product_id=product_id,
        warehouse_id=from_warehouse_id,
        transaction_type="TRANSFER_OUT",
        quantity=quantity,
        reference_entity="inventory_transfer",
        user_id=user_id,
        transaction_metadata={
            "to_warehouse_id": to_warehouse_id
        }
    )

    destination_transaction = InventoryTransaction(
        product_id=product_id,
        warehouse_id=to_warehouse_id,
        transaction_type="TRANSFER_IN",
        quantity=quantity,
        reference_entity="inventory_transfer",
        user_id=user_id,
        transaction_metadata={
            "from_warehouse_id": from_warehouse_id
        }
    )

    db.add(source_transaction)
    db.add(destination_transaction)

    db.commit()

    db.refresh(source_inventory)
    db.refresh(destination_inventory)

    return {
        "product_id": product_id,
        "from_warehouse_id": from_warehouse_id,
        "to_warehouse_id": to_warehouse_id,
        "quantity": quantity
    }