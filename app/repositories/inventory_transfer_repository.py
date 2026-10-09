from sqlalchemy.orm import Session

from app.models.inventory import Inventory


def get_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int
):
    return (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id,
            Inventory.warehouse_id == warehouse_id
        )
        .with_for_update()
        .first()
    )