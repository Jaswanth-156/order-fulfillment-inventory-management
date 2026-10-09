from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class OrderAssignment(Base):
    __tablename__ = "order_assignments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)

    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    order = relationship("Order")
    agent = relationship("User",foreign_keys=[agent_id])
    assigner = relationship("User",foreign_keys=[assigned_by])