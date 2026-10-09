from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=True)
    action = Column(String(100),nullable=False)
    entity_type = Column(String(50),nullable=False)
    entity_id = Column(Integer,nullable=True)
    details = Column(JSON,nullable=True)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    user = relationship("User")