import uuid
from typing import List, Optional
from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Schedule
from src.schedules.schemas import ScheduleCreate, ScheduleUpdate


async def get_all_schedules(skip: int = 0, limit: int = 100, session: AsyncSession = None, day_of_week: int = None, barbershop_id: uuid.UUID = None, sort_by: str = "created_at", order: str = "desc") -> List[Schedule]:
    statement = select(Schedule)
    if day_of_week is not None:
        statement = statement.where(Schedule.day_of_week == day_of_week)
    if barbershop_id:
        statement = statement.where(Schedule.barbershop_id == barbershop_id)
    order_func = desc if order == "desc" else asc
    if hasattr(Schedule, sort_by):
        statement = statement.order_by(order_func(getattr(Schedule, sort_by)))
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_schedule_by_id(schedule_id: uuid.UUID, session: AsyncSession) -> Optional[Schedule]:
    result = await session.execute(
        select(Schedule).where(Schedule.uid == schedule_id)
    )
    return result.scalar_one_or_none()


async def create_schedule(schedule_data: ScheduleCreate, session: AsyncSession) -> Schedule:
    new_schedule = Schedule(
        user_id=schedule_data.user_id,
        barbershop_id=schedule_data.barbershop_id,
        day_of_week=schedule_data.day_of_week,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time
    )
    session.add(new_schedule)
    await session.commit()
    await session.refresh(new_schedule)
    return new_schedule


async def update_schedule(schedule_id: uuid.UUID, update_data: ScheduleUpdate, session: AsyncSession) -> Optional[
    Schedule]:
    sched = await get_schedule_by_id(schedule_id, session)
    if not sched:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(sched, key, value)
    await session.commit()
    await session.refresh(sched)
    return sched


async def delete_schedule(schedule_id: uuid.UUID, session: AsyncSession) -> bool:
    sched = await get_schedule_by_id(schedule_id, session)
    if not sched:
        return False
    await session.delete(sched)
    await session.commit()
    return True
