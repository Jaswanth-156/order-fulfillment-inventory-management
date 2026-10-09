from datetime import timezone

from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.models.return_model import Return
from app.models.return_item import ReturnItem
from app.models.order import Order
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from app.repositories import return_repository


def create_return(
    db: Session,
    order_id: int,
    customer_id: int,
    reason: str,
    items: list
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.customer_id == customer_id
        )
        .first()
    )

    if not order:
        raise ValueError("Order not found")

    if order.status != "DELIVERED":
        raise ValueError("Return can only be requested for delivered orders")

    return_request = Return(
        order_id=order_id,
        customer_id=customer_id,
        reason=reason,
        status="Requested"
    )

    return_repository.create_return(db, return_request)

    for item in items:
        order_item = (
            db.query(OrderItem)
            .filter(
                OrderItem.order_id == order_id,
                OrderItem.product_id == item.product_id
            )
            .first()
        )

        if not order_item:
            raise ValueError(
                f"Product {item.product_id} is not part of this order"
            )

        if item.quantity > order_item.quantity:
            raise ValueError(
                f"Return quantity cannot exceed ordered quantity for product {item.product_id}"
            )

        return_item = ReturnItem(
            return_id=return_request.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(return_item)

    db.commit()
    db.refresh(return_request)

    return return_request


def update_return_status(
    db: Session,
    return_id: int,
    new_status: str,
    processed_by: int
):
    return_request = return_repository.get_return_by_id(
        db,
        return_id
    )

    if not return_request:
        raise ValueError("Return not found")

    allowed_transitions = {
        "Requested": ["Approved", "Rejected"],
        "Approved": ["Received"],
        "Received": ["Refunded"],
        "Rejected": [],
        "Refunded": []
    }

    current_status = return_request.status

    if new_status not in allowed_transitions.get(current_status, []):
        raise ValueError(
            f"Cannot change return status from {current_status} to {new_status}"
        )

    if new_status == "Received":
        order = (
            db.query(Order)
            .filter(Order.id == return_request.order_id)
            .first()
        )

        if not order:
            raise ValueError("Order not found")

        for item in return_request.items:
            inventory = (
                db.query(Inventory)
                .filter(
                    Inventory.product_id == item.product_id,
                    Inventory.warehouse_id == order.warehouse_id
                )
                .with_for_update()
                .first()
            )

            if not inventory:
                raise ValueError(
                    f"Inventory not found for product {item.product_id}"
                )

            inventory.available_quantity += item.quantity

            transaction = InventoryTransaction(
                product_id=item.product_id,
                warehouse_id=order.warehouse_id,
                transaction_type="RETURN",
                quantity=item.quantity,
                reference_entity="return",
                reference_id=return_request.id,
                user_id=processed_by
            )

            db.add(transaction)

    return_request.status = new_status
    return_request.processed_by = processed_by

    if new_status in ["Received", "Refunded"]:
        from datetime import datetime
        return_request.processed_at = datetime.now(timezone.utc)()

    db.commit()
    db.refresh(return_request)

    return return_request