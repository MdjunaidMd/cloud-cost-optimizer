# backend/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema for input (what client sends)
class UsageCreate(BaseModel):
    cloud_provider: str
    service_name: str
    resource_id: str
    usage_amount: float
    cost: float

# Schema for output (what API returns)
class UsageOut(UsageCreate):
    id: int
    timestamp: Optional[datetime]

    class Config:
        orm_mode = True
