from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderAssignmentCreate(BaseModel):
    order_id: int
    agent_id: int


class OrderAssignmentResponse(BaseModel):
    id: int
    order_id: int
    agent_id: int
    assigned_at: datetime
    assigned_by: int

    model_config = ConfigDict(from_attributes=True)