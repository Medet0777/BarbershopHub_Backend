import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    barbershop_id: uuid.UUID
    booking_id: uuid.UUID
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(ReviewBase):
    uid: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
