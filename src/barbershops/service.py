import uuid
from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Barbershop
from src.barbershops.schemas import BarbershopCreate, BarbershopUpdate


async def get_all_barbershops(skip: int = 0, limit: int = 100, session: AsyncSession = None) -> List[Barbershop]:
    result = await session.execute(
        select(Barbershop).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_barbershop_by_id(shop_id: uuid.UUID, session: AsyncSession) -> Optional[Barbershop]:
    result = await session.execute(
        select(Barbershop).where(Barbershop.uid == shop_id)
    )
    return result.scalar_one_or_none()


async def create_barbershop(shop_data: BarbershopCreate, session: AsyncSession) -> Barbershop:
    new_shop = Barbershop(
        name=shop_data.name,
        address=shop_data.address,
        phone=shop_data.phone,
        email=shop_data.email,
        owner_id=shop_data.owner_id
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
    await session.delete(shop)
    await session.commit()
    return True
