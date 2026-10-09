from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class Return(Base):
    __tablename__ = "returns"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="Requested")
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    processed_at = Column(DateTime, nullable=True)
    order = relationship("Order")
    customer = relationship("User", foreign_keys=[customer_id])
    processor = relationship("User", foreign_keys=[processed_by])
    items = relationship("ReturnItem",back_populates="return_request",cascade="all, delete-orphan")