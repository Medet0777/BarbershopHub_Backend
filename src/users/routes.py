import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency, verify_admin_role
from src.db.session import get_session
from src.users import service
from src.users.schemas import UserCreate, UserOut, UserUpdate

user_router = APIRouter()


@user_router.get("/", response_model=List[UserOut])
async def get_users(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session)
):
    users = await service.get_all_users(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session
    )
    return users


@user_router.get("/{user_id}", response_model=UserOut)
async def get_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    user = await service.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    new_user = await service.create_user(user_data, session)
    return new_user


@user_router.patch(
    "/{user_id}",
    response_model=UserOut
)
async def update_user(
        user_id: uuid.UUID,
        update_data: UserUpdate,
        session: AsyncSession = Depends(get_session)
):
    user = await service.update_user(user_id, update_data, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_admin_role)]
)
async def delete_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    deleted = await service.delete_user(user_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {}
