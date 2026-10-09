
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReturnItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class ReturnCreate(BaseModel):
    order_id: int
    reason: str = Field(min_length=1, max_length=500)
    items: list[ReturnItemCreate] = Field(min_length=1)


class ReturnStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=30)


class ReturnItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    return_id: int
    product_id: int
    quantity: int


class ReturnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    customer_id: int
    reason: str
    status: str
    processed_by: int | None
    created_at: datetime
    processed_at: datetime | None
    items: list[ReturnItemResponse] = []