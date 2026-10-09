from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.order import Order
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.models.inventory import Inventory


def get_dashboard(db: Session):

    total_orders = db.query(func.count(Order.id)).scalar()

    pending_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == "PENDING")
        .scalar()
    )

    processing_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == "PROCESSING")
        .scalar()
    )

    shipped_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == "SHIPPED")
        .scalar()
    )

    delivered_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == "DELIVERED")
        .scalar()
    )

    cancelled_orders = (
        db.query(func.count(Order.id))
        .filter(Order.status == "CANCELLED")
        .scalar()
    )

    total_products = db.query(func.count(Product.id)).scalar()

    low_stock_items = (
        db.query(func.count(Inventory.id))
        .filter(
            Inventory.available_quantity <= Inventory.reorder_level
        )
        .scalar()
    )

    total_warehouses = db.query(func.count(Warehouse.id)).scalar()

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "total_products": total_products,
        "low_stock_items": low_stock_items,
        "total_warehouses": total_warehouses
    }