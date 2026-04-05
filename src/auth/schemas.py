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
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str = Field(min_length=6)
    confirm_new_password: str = Field(min_length=6)
