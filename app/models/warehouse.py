from sqlalchemy import Column, DateTime, Integer, String, Boolean
from datetime import datetime, timezone
from app.db.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at=Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    updated_at=Column(DateTime,default=datetime.now(timezone.utc),onupdate=datetime.now(timezone.utc),nullable=False)
    
