from sqlalchemy.orm import Session

from app.models.inventory_transaction import InventoryTransaction


def create_transaction(
    db: Session,
    transaction: InventoryTransaction
):
    db.add(transaction)
    db.flush()
    return transaction

def get_transactions(db: Session):
    return (
        db.query(InventoryTransaction)
        .order_by(InventoryTransaction.created_at.desc())
        .all()
    )
