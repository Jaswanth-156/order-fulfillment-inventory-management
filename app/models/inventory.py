from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0, nullable=False)
    damaged_quantity = Column(Integer, default=0, nullable=False)
    reorder_level = Column(Integer, default=0, nullable=False)

    updated_at = Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc),nullable=False)

    product = relationship("Product")
    warehouse = relationship("Warehouse")

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "warehouse_id",
            name="uq_inventory_product_warehouse"
        ),
    )