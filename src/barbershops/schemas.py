from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class BarbershopBase(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    owner_id: uuid.UUID


class BarbershopCreate(BarbershopBase):
    pass


class BarbershopUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class BarbershopOut(BarbershopBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
