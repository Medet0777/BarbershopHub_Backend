import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.db.enums import RoleEnum


class UserCreateModel(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)
    role: Optional[RoleEnum] = RoleEnum.CLIENT


class UserLoginModel(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime
