from sqlalchemy.orm import Session
from app.models.warehouse import Warehouse


def create_warehouse(db: Session, warehouse: Warehouse):
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


def get_warehouses(db: Session):
    return db.query(Warehouse).all()


def get_warehouse_by_id(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def update_warehouse(db: Session, warehouse: Warehouse):
    db.commit()
    db.refresh(warehouse)
    return warehouse