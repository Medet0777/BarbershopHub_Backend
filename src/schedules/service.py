import uuid
from typing import List, Optional
from sqlmodel import select, desc, asc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.db.models import Schedule, Booking
from src.schedules.schemas import ScheduleCreate, ScheduleUpdate


async def get_all_schedules(
        skip: int = 0, limit: int = 100, session: AsyncSession = None,
        day_of_week: int = None, barbershop_id: uuid.UUID = None,
        sort_by: str = "created_at", order: str = "desc",
) -> List[Schedule]:
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


async def _check_overlap(session: AsyncSession, user_id, barbershop_id, day_of_week, start_time, end_time,
                         exclude_id=None):
    """Check for overlapping schedules for the same barber on the same day."""
    statement = select(Schedule).where(
        and_(
            Schedule.user_id == user_id,
            Schedule.barbershop_id == barbershop_id,
            Schedule.day_of_week == day_of_week,
            Schedule.start_time < end_time,
            Schedule.end_time > start_time,
        )
    )
    if exclude_id:
        statement = statement.where(Schedule.uid != exclude_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_schedule(schedule_data: ScheduleCreate, session: AsyncSession) -> Schedule:
    # Validate day_of_week 0-6
    if schedule_data.day_of_week < 0 or schedule_data.day_of_week > 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="day_of_week must be between 0 and 6")

    # start_time must be before end_time
    if schedule_data.start_time >= schedule_data.end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="start_time must be before end_time")

    # Check for overlapping schedules
    overlap = await _check_overlap(
        session, schedule_data.user_id, schedule_data.barbershop_id,
        schedule_data.day_of_week, schedule_data.start_time, schedule_data.end_time,
    )
    if overlap:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Schedule overlaps with an existing one")

    new_schedule = Schedule(
        user_id=schedule_data.user_id,
        barbershop_id=schedule_data.barbershop_id,
        day_of_week=schedule_data.day_of_week,
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
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

    update_dict = update_data.model_dump(exclude_unset=True)

    # Apply updates temporarily for validation
    new_day = update_dict.get("day_of_week", sched.day_of_week)
    new_start = update_dict.get("start_time", sched.start_time)
    new_end = update_dict.get("end_time", sched.end_time)
    new_user = update_dict.get("user_id", sched.user_id)
    new_barbershop = update_dict.get("barbershop_id", sched.barbershop_id)

    if new_day < 0 or new_day > 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="day_of_week must be between 0 and 6")

    if new_start >= new_end:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="start_time must be before end_time")

    overlap = await _check_overlap(session, new_user, new_barbershop, new_day, new_start, new_end,
                                   exclude_id=schedule_id)
    if overlap:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Schedule overlaps with an existing one")

    for key, value in update_dict.items():
        setattr(sched, key, value)
    await session.commit()
    await session.refresh(sched)
    return sched


async def delete_schedule(schedule_id: uuid.UUID, session: AsyncSession) -> bool:
    sched = await get_schedule_by_id(schedule_id, session)
    if not sched:
        return False

    # Check for active bookings
    result = await session.execute(
        select(Booking).where(
            and_(
                Booking.schedule_id == schedule_id,
                Booking.status.in_(["Pending", "Confirmed"]),
            )
        )
    )
    active_booking = result.scalar_one_or_none()
    if active_booking:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot delete schedule with active bookings")

    await session.delete(sched)
    await session.commit()
    return True
