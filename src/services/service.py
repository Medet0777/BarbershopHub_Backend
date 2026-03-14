import uuid
from typing import List, Optional
from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Service
from src.services.schemas import ServiceCreate, ServiceUpdate


async def get_all_services(skip: int = 0, limit: int = 100, session: AsyncSession = None, search: str = None, category: str = None, sort_by: str = "created_at", order: str = "desc") -> List[Service]:
    statement = select(Service)
    if search:
        statement = statement.where(Service.name.ilike(f"%{search}%"))
    if category:
        statement = statement.where(Service.category == category)
    order_func = desc if order == "desc" else asc
    if hasattr(Service, sort_by):
        statement = statement.order_by(order_func(getattr(Service, sort_by)))
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_service_by_id(service_id: uuid.UUID, session: AsyncSession) -> Optional[Service]:
    result = await session.execute(
        select(Service).where(Service.uid == service_id)
    )
    return result.scalar_one_or_none()


async def create_service(service_data: ServiceCreate, session: AsyncSession) -> Service:
    new_service = Service(
        name=service_data.name,
        description=service_data.description,
        category=service_data.category,
        duration_minutes=service_data.duration_minutes,
        price=service_data.price,
        barbershop_id=service_data.barbershop_id
    )
    session.add(new_service)
    await session.commit()
    await session.refresh(new_service)
    return new_service


async def update_service(service_id: uuid.UUID, update_data: ServiceUpdate, session: AsyncSession) -> Optional[Service]:
    service_obj = await get_service_by_id(service_id, session)
    if not service_obj:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(service_obj, key, value)
    await session.commit()
    await session.refresh(service_obj)
    return service_obj


async def delete_service(service_id: uuid.UUID, session: AsyncSession) -> bool:
    service_obj = await get_service_by_id(service_id, session)
    if not service_obj:
        return False
    await session.delete(service_obj)
    await session.commit()
    return True
