import uuid
from typing import List, Optional
from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import and_
from fastapi import HTTPException, status

from src.db.models import Barbershop, Booking, Schedule
from src.barbershops.schemas import BarbershopCreate, BarbershopUpdate


async def get_all_barbershops(skip: int = 0, limit: int = 100, session: AsyncSession = None, search: str = None, sort_by: str = "created_at", order: str = "desc") -> List[Barbershop]:
    statement = select(Barbershop)
    if search:
        statement = statement.where(
            Barbershop.name.ilike(f"%{search}%") | Barbershop.address.ilike(f"%{search}%")
        )
    order_func = desc if order == "desc" else asc
    if hasattr(Barbershop, sort_by):
        statement = statement.order_by(order_func(getattr(Barbershop, sort_by)))
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_barbershop_by_id(shop_id: uuid.UUID, session: AsyncSession) -> Optional[Barbershop]:
    result = await session.execute(
        select(Barbershop).where(Barbershop.uid == shop_id)
    )
    return result.scalar_one_or_none()


async def create_barbershop(shop_data: BarbershopCreate, session: AsyncSession) -> Barbershop:
    # Check duplicate name + address
    result = await session.execute(
        select(Barbershop).where(
            and_(
                Barbershop.name == shop_data.name,
                Barbershop.address == shop_data.address,
            )
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Barbershop with this name and address already exists")

    new_shop = Barbershop(
        name=shop_data.name,
        address=shop_data.address,
        phone=shop_data.phone,
        email=shop_data.email,
        owner_id=shop_data.owner_id,
    )
    session.add(new_shop)
    await session.commit()
    await session.refresh(new_shop)
    return new_shop


async def update_barbershop(shop_id: uuid.UUID, update_data: BarbershopUpdate, session: AsyncSession) -> Optional[
    Barbershop]:
    shop = await get_barbershop_by_id(shop_id, session)
    if not shop:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(shop, key, value)
    await session.commit()
    await session.refresh(shop)
    return shop


async def delete_barbershop(shop_id: uuid.UUID, session: AsyncSession) -> bool:
    shop = await get_barbershop_by_id(shop_id, session)
    if not shop:
        return False

    # Check for active bookings via schedules
    result = await session.execute(
        select(Booking).join(Schedule).where(
            and_(
                Schedule.barbershop_id == shop_id,
                Booking.status.in_(["Pending", "Confirmed"]),
            )
        )
    )
    active = result.scalar_one_or_none()
    if active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete barbershop with active bookings")

    await session.delete(shop)
    await session.commit()
    return True
