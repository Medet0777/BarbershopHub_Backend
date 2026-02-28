from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class BarbershopBase(BaseModel):
    name: str
    address: str
    phone: str
    email: str


class BarbershopCreate(BarbershopBase):
    pass


class BarbershopUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]


class BarbershopOut(BarbershopBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
