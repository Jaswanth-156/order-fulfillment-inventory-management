from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ReturnItem(Base):
    __tablename__ = "return_items"
    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(Integer,ForeignKey("returns.id"),nullable=False)
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    return_request = relationship("Return",back_populates="items")
    product = relationship("Product")