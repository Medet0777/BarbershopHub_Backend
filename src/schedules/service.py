import uuid
from datetime import datetime, timezone
from typing import List, Optional

from src.schedules.schedules_data import schedules
from src.schedules.schemas import ScheduleCreate, ScheduleUpdate


def get_all_schedules(
        skip: int = 0, limit: int = 100
) -> List[dict]:
    return schedules[skip:skip + limit]


def get_schedule_by_id(schedule_id: uuid.UUID) -> Optional[dict]:
    for schedule in schedules:
        if schedule["uid"] == schedule_id:
            return schedule
    return None


def create_schedule(schedule_data: ScheduleCreate) -> dict:
    new_schedule = {
        "uid": uuid.uuid4(),
        "user_id": schedule_data.user_id,
        "day_of_week": schedule_data.day_of_week,
        "start_time": schedule_data.start_time,
        "end_time": schedule_data.end_time,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    schedules.append(new_schedule)
    return new_schedule


def update_schedule(schedule_id: uuid.UUID, update_data: ScheduleUpdate) -> Optional[dict]:
    sched = get_schedule_by_id(schedule_id)
    if not sched:
        return None

    for key, value in update_data.model_dump(exclude_unset=True).items():
        sched[key] = value
    sched["updated_at"] = datetime.now(timezone.utc)
    return sched


def delete_schedule(schedule_id: uuid.UUID) -> bool:
    sched = get_schedule_by_id(schedule_id)
    if not sched:
        return False
    schedules.remove(sched)
    return True