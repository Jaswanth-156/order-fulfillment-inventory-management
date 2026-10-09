from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer,ForeignKey("orders.id"),nullable=False)
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    unit_price = Column(Numeric(12, 2),nullable=False)
    discount = Column(Numeric(12, 2),nullable=False,default=0)
    tax = Column(Numeric(12, 2),nullable=False,default=0)
    total = Column(Numeric(12, 2),nullable=False)
    order = relationship("Order",back_populates="items")
    product = relationship("Product")