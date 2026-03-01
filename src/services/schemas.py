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
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None


class ServiceOut(ServiceBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
