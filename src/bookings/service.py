import uuid
from typing import List, Optional
from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Booking, Service, Schedule
from src.bookings.schemas import BookingCreate, BookingUpdate
from fastapi import HTTPException, status


VALID_STATUS_TRANSITIONS = {
    "Pending": ["Confirmed", "Cancelled"],
    "Confirmed": ["Completed", "Cancelled"],
    "Completed": [],
    "Cancelled": [],
}


async def get_all_bookings(
    skip: int = 0, limit: int = 100, session: AsyncSession = None,
    status_filter: str = None, sort_by: str = "created_at", order: str = "desc",
) -> List[Booking]:
    statement = select(Booking)
    if status_filter:
        statement = statement.where(Booking.status == status_filter)
    order_func = desc if order == "desc" else asc
    if hasattr(Booking, sort_by):
        statement = statement.order_by(order_func(getattr(Booking, sort_by)))
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_booking_by_id(booking_id: uuid.UUID, session: AsyncSession) -> Optional[Booking]:
    result = await session.execute(
        select(Booking).where(Booking.uid == booking_id)
    )
    return result.scalar_one_or_none()


async def create_booking(booking_data: BookingCreate, session: AsyncSession) -> Booking:
    # Check service exists
    svc_result = await session.execute(select(Service).where(Service.uid == booking_data.service_id))
    service_obj = svc_result.scalar_one_or_none()
    if not service_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

    # Check schedule exists
    sched_result = await session.execute(select(Schedule).where(Schedule.uid == booking_data.schedule_id))
    schedule_obj = sched_result.scalar_one_or_none()
    if not schedule_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    # Service must belong to same barbershop as schedule
    if service_obj.barbershop_id != schedule_obj.barbershop_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service and schedule must belong to the same barbershop")

    new_booking = Booking(
        user_id=booking_data.user_id,
        service_id=booking_data.service_id,
        schedule_id=booking_data.schedule_id,
        status=booking_data.status or "Pending",
    )
    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)
    return new_booking


async def update_booking(booking_id: uuid.UUID, update_data: BookingUpdate, session: AsyncSession) -> Optional[Booking]:
    bk = await get_booking_by_id(booking_id, session)
    if not bk:
        return None

    # Validate status transition
    update_dict = update_data.model_dump(exclude_unset=True)
    if "status" in update_dict:
        new_status = update_dict["status"]
        allowed = VALID_STATUS_TRANSITIONS.get(bk.status, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from '{bk.status}' to '{new_status}'. Allowed: {allowed}",
            )

    # Cannot update completed or cancelled booking (except status by admin)
    if bk.status in ["Completed", "Cancelled"]:
        non_status_keys = [k for k in update_dict if k != "status"]
        if non_status_keys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot modify a {bk.status.lower()} booking",
            )

    for key, value in update_dict.items():
        setattr(bk, key, value)
    await session.commit()
    await session.refresh(bk)
    return bk


async def delete_booking(booking_id: uuid.UUID, session: AsyncSession) -> bool:
    bk = await get_booking_by_id(booking_id, session)
    if not bk:
        return False
    await session.delete(bk)
    await session.commit()
    return True
