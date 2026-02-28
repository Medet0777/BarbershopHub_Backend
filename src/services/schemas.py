from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class ServiceBase(BaseModel):
    name: str
    description: Optional[str]
    category: str
    duration_minutes: Optional[int] = 30
    price: Optional[float] = 0.0


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    duration_minutes: Optional[int]
    price: Optional[float]


class ServiceOut(ServiceBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
