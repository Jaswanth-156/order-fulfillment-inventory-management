from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    transaction_type = Column(String(30), nullable=False)
    quantity = Column(Integer, nullable=False)
    reference_entity = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    transaction_metadata = Column(JSON, nullable=True)
    product = relationship("Product")
    warehouse = relationship("Warehouse")
    user = relationship("User")