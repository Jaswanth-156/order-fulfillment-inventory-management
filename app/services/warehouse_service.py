from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.repositories import warehouse_repository


def create_warehouse(
    db: Session,
    name: str,
    location: str,
    capacity: int
):
    warehouse = Warehouse(
        name=name,
        location=location,
        capacity=capacity
    )

    return warehouse_repository.create_warehouse(db, warehouse)


def get_warehouses(db: Session):
    return warehouse_repository.get_warehouses(db)


def get_warehouse(db: Session, warehouse_id: int):
    warehouse = warehouse_repository.get_warehouse_by_id(db, warehouse_id)

    if not warehouse:
        raise ValueError("Warehouse not found")

    return warehouse


def update_warehouse(
    db: Session,
    warehouse_id: int,
    name: str | None = None,
    location: str | None = None,
    capacity: int | None = None
):
    warehouse = warehouse_repository.get_warehouse_by_id(db, warehouse_id)

    if not warehouse:
        raise ValueError("Warehouse not found")

    if name is not None:
        warehouse.name = name

    if location is not None:
        warehouse.location = location

    if capacity is not None:
        warehouse.capacity = capacity

    return warehouse_repository.update_warehouse(db, warehouse)


def activate_warehouse(db: Session, warehouse_id: int):
    warehouse = warehouse_repository.get_warehouse_by_id(db, warehouse_id)

    if not warehouse:
        raise ValueError("Warehouse not found")

    warehouse.is_active = True

    return warehouse_repository.update_warehouse(db, warehouse)


def deactivate_warehouse(db: Session, warehouse_id: int):
    warehouse = warehouse_repository.get_warehouse_by_id(db, warehouse_id)

    if not warehouse:
        raise ValueError("Warehouse not found")

    warehouse.is_active = False

    return warehouse_repository.update_warehouse(db, warehouse)