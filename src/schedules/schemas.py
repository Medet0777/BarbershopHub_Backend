from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, time


class ScheduleBase(BaseModel):
    user_id: uuid.UUID
    day_of_week: int  # 0 = Monday, 6 = Sunday
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class ScheduleOut(ScheduleBase):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
