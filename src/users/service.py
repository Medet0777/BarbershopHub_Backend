import uuid
from typing import Optional, List

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from src.db.models import User
from src.users.schemas import UserCreate, UserUpdate


async def get_all_users(skip: int = 0, limit: int = 100, session: AsyncSession = None) -> List[User]:
    result = await session.execute(
        select(User).offset(skip).limit(limit)
    )
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return user


async def delete_user(user_id: uuid.UUID, session: AsyncSession) -> bool:
    user = await get_user_by_id(user_id, session)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True