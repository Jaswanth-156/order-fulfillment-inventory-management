from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class InventoryTransactionResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    transaction_type: str
    quantity: int
    reference_entity: str | None
    reference_id: int | None
    user_id: int | None
    created_at: datetime
    transaction_metadata: dict[str, Any] | None

    model_config = ConfigDict(from_attributes=True)