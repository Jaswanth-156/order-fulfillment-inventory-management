
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    warehouse_id: int
    expected_delivery_date: datetime | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    customer_id: int
    warehouse_id: int
    total_amount: Decimal
    status: str
    payment_status: str
    expected_delivery_date: datetime | None
    created_at: datetime
    updated_at: datetime


class OrderStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=30)