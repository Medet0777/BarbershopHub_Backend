from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from src.db.enums import BookingStatusEnum


class BookingBase(BaseModel):
    user_id: uuid.UUID
    service_id: uuid.UUID
    schedule_id: uuid.UUID
    status: Optional[BookingStatusEnum] = BookingStatusEnum.PENDING

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    service_id: Optional[uuid.UUID] = None
    schedule_id: Optional[uuid.UUID] = None
    status: Optional[BookingStatusEnum] = BookingStatusEnum.PENDING

class BookingOut(BookingBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime