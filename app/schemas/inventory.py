from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    available_quantity: int
    reserved_quantity: int
    damaged_quantity: int
    reorder_level: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InventoryAdjustRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int
    reason: str = Field(min_length=1, max_length=255)
    reorder_level: int = Field(default=0, ge=0)


class InventoryTransferRequest(BaseModel):
    product_id: int
    from_warehouse_id: int
    to_warehouse_id: int
    quantity: int = Field(gt=0)


class InventoryReserveRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(gt=0)

class InventoryReleaseRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(gt=0)