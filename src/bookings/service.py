import uuid
from typing import List, Optional
from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Booking
from src.bookings.schemas import BookingCreate, BookingUpdate


async def get_all_bookings(skip: int = 0, limit: int = 100, session: AsyncSession = None, status_filter: str = None, sort_by: str = "created_at", order: str = "desc") -> List[Booking]:
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
    new_booking = Booking(
        user_id=booking_data.user_id,
        service_id=booking_data.service_id,
        schedule_id=booking_data.schedule_id,
        status=booking_data.status or "Pending"
    )
    session.add(new_booking)
    await session.commit()
    await session.refresh(new_booking)
    return new_booking


async def update_booking(booking_id: uuid.UUID, update_data: BookingUpdate, session: AsyncSession) -> Optional[Booking]:
    bk = await get_booking_by_id(booking_id, session)
    if not bk:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
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
