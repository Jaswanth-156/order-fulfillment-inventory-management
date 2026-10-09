from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    title = Column(String(150),nullable=False)
    message = Column(Text,nullable=False)
    notification_type = Column(String(50),nullable=False)
    is_read = Column(Boolean,default=False,nullable=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)

    user = relationship("User")