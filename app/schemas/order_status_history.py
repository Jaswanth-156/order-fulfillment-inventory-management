
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderStatusHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    old_status: str | None
    new_status: str
    changed_by: int
    created_at: datetime
