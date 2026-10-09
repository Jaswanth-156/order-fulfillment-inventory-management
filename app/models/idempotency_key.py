from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255),unique=True,nullable=False,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    request_hash = Column(String(255),nullable=False)
    response_status = Column(Integer,nullable=True)
    response_body = Column(Text,nullable=True)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)

    user = relationship("User")