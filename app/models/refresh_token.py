from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    token = Column(String(500),unique=True,nullable=False)
    expires_at = Column(DateTime,nullable=False)
    is_revoked = Column(Boolean,default=False,nullable=False)

    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)

    user = relationship("User")