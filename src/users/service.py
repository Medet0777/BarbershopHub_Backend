import uuid
from typing import Optional, List

from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.db.models import User
from src.users.schemas import UserCreate, UserUpdate
from src.errors import UserAlreadyExists


async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    sort_by: str = "created_at",
    order: str = "desc",
    session: AsyncSession = None,
) -> List[User]:
    statement = select(User)

    if search:
        statement = statement.where(
            User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")
        )

    order_func = desc if order == "desc" else asc
    if hasattr(User, sort_by):
        statement = statement.order_by(order_func(getattr(User, sort_by)))

    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_user_by_id(user_id: uuid.UUID, session: AsyncSession) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.uid == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role
    )
    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExists()

    return new_user


async def update_user(user_id: uuid.UUID, update_data: UserUpdate, session: AsyncSession) -> Optional[User]:
    user = await get_user_by_id(user_id, session)
    if not user:
        return None

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    try:
        await session.commit()
        await session.refresh(user)
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExists()

    return user


async def delete_user(user_id: uuid.UUID, session: AsyncSession) -> bool:
    user = await get_user_by_id(user_id, session)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True
