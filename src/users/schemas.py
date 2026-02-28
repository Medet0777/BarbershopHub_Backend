from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    role: Optional[str] = "client"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[str]


class UserOut(UserBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
