import hashlib
import json

from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.repositories import order_repository

from app.services.idempotency_service import create_key, get_existing_key, save_response
from app.services.inventory_service import reserve_inventory

def create_order(
    db: Session,
    customer_id: int,
    warehouse_id: int,
    items: list,
    expected_delivery_date=None,
    idempotency_key: str | None = None
):
    request_data = {
        "customer_id": customer_id,
        "warehouse_id": warehouse_id,
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity
            }
            for item in items
        ],
        "expected_delivery_date": str(expected_delivery_date)
        if expected_delivery_date
        else None
    }

    request_hash = hashlib.sha256(
        json.dumps(request_data, sort_keys=True).encode()
    ).hexdigest()

    if idempotency_key:
        existing_key = get_existing_key(db, idempotency_key)

        if existing_key:
            if existing_key.user_id != customer_id:
                raise ValueError("Invalid idempotency key")

            if existing_key.request_hash != request_hash:
                raise ValueError(
                    "Idempotency key already used with a different request"
                )

            if existing_key.response_body:
                return json.loads(existing_key.response_body)

    if idempotency_key:
        create_key(
            db=db,
            key=idempotency_key,
            user_id=customer_id,
            request_hash=request_hash
        )

    order = Order(
        order_number="TEMP",
        customer_id=customer_id,
        warehouse_id=warehouse_id,
        total_amount=0,
        status="PENDING",
        payment_status="PENDING",
        expected_delivery_date=expected_delivery_date
    )

    db.add(order)
    db.flush()

    order.order_number = f"ORD-{order.id:06d}"

    total_amount = 0

    for item in items:
        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id,
                Product.is_active == True
            )
            .first()
        )

        if not product:
            raise ValueError(
                f"Product {item.product_id} not found or inactive"
            )

        line_total = product.price * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            discount=0,
            tax=0,
            total=line_total
        )

        db.add(order_item)

        reserve_inventory(
            db=db,
            product_id=product.id,
            warehouse_id=warehouse_id,
            quantity=item.quantity,
            user_id=customer_id
        )

        total_amount += line_total

    order.total_amount = total_amount

    db.commit()
    db.refresh(order)

    if idempotency_key:
        response_body = json.dumps(
            {
                "id": order.id,
                "order_number": order.order_number,
                "customer_id": order.customer_id,
                "warehouse_id": order.warehouse_id,
                "total_amount": float(order.total_amount),
                "status": order.status,
                "payment_status": order.payment_status,
                "expected_delivery_date": (
                    order.expected_delivery_date.isoformat()
                    if order.expected_delivery_date
                    else None
                ),
                "created_at": order.created_at.isoformat(),
                "updated_at": order.updated_at.isoformat()
            }
        )

        save_response(
            db=db,
            idempotency_key=get_existing_key(db, idempotency_key),
            response_status=200,
            response_body=response_body
        )

        db.commit()

    return order

def cancel_order(
    db: Session,
    order_id: int,
    cancelled_by: int
):
    order = order_repository.get_order_by_id(db, order_id)

    if not order:
        raise ValueError("Order not found")

    if order.status not in ["PENDING", "CONFIRMED", "PROCESSING"]:
        raise ValueError(
            f"Order cannot be cancelled in {order.status} status"
        )

    for item in order.items:
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

        if inventory.reserved_quantity < item.quantity:
            raise ValueError(
                f"Reserved inventory is insufficient for product {item.product_id}"
            )

    old_status = order.status

    for item in order.items:
        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == item.product_id,
                Inventory.warehouse_id == order.warehouse_id
            )
            .with_for_update()
            .first()
        )

        inventory.available_quantity += item.quantity
        inventory.reserved_quantity -= item.quantity

        transaction = InventoryTransaction(
            product_id=item.product_id,
            warehouse_id=order.warehouse_id,
            transaction_type="RELEASE",
            quantity=item.quantity,
            reference_entity="order",
            reference_id=order.id,
            user_id=cancelled_by
        )

        db.add(transaction)

    order.status = "CANCELLED"

    from app.models.order_status_history import OrderStatusHistory

    history = OrderStatusHistory(
        order_id=order.id,
        old_status=old_status,
        new_status="CANCELLED",
        changed_by=cancelled_by
    )

    db.add(history)

    db.commit()
    db.refresh(order)

    return order


def update_order_status(
    db: Session,
    order_id: int,
    new_status: str,
    changed_by: int
):
    order = order_repository.get_order_by_id(db, order_id)

    if not order:
        raise ValueError("Order not found")

    allowed_transitions = {
        "PENDING": ["CONFIRMED", "CANCELLED"],
        "CONFIRMED": ["PROCESSING", "CANCELLED"],
        "PROCESSING": ["PACKED", "CANCELLED"],
        "PACKED": ["SHIPPED", "CANCELLED"],
        "SHIPPED": ["DELIVERED"],
        "DELIVERED": [],
        "CANCELLED": []
    }

    current_status = order.status

    if new_status not in allowed_transitions.get(current_status, []):
        raise ValueError(
            f"Cannot change order status from {current_status} to {new_status}"
        )

    old_status = order.status
    order.status = new_status

    from app.models.order_status_history import OrderStatusHistory

    history = OrderStatusHistory(
        order_id=order.id,
        old_status=old_status,
        new_status=new_status,
        changed_by=changed_by
    )

    db.add(history)
    db.commit()
    db.refresh(order)

    return order