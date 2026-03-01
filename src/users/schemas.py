from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from src.db.enums import RoleEnum


class UserBase(BaseModel):
    name: str
    email: str
    role: Optional[RoleEnum] = RoleEnum.CLIENT


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = RoleEnum.CLIENT


class UserOut(UserBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
