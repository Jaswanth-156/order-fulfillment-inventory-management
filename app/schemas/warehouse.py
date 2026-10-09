from datetime import datetime
from pydantic import BaseModel, ConfigDict,Field

class WarehouseCreate(BaseModel):
    name:str=Field(min_length=1,max_length=100)
    location:str=Field(min_length=1,max_length=255)
    capacity:int=Field(gt=0)

class WarehouseUpdate(BaseModel):
    name:str|None=Field(default=None,min_length=1,max_length=100)
    location:str|None=Field(default=None,min_length=1,max_length=255)
    capacity:int|None=Field(default=None,gt=0)

class WarehouseResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)