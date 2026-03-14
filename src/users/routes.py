import uuid
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.users import service
from src.users.schemas import UserCreate, UserOut, UserUpdate
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import UserNotFound

user_router = APIRouter()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))


@user_router.get("/", response_model=List[UserOut], dependencies=[admin_role_checker])
async def get_users(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session),
):
    users = await service.get_all_users(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session
    )
    return users


@user_router.get("/{user_id}", response_model=UserOut, dependencies=[admin_role_checker])
async def get_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    user = await service.get_user_by_id(user_id, session)
    if not user:
        raise UserNotFound()
    return user


@user_router.patch(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[admin_role_checker],
)
async def update_user(
        user_id: uuid.UUID,
        update_data: UserUpdate,
        session: AsyncSession = Depends(get_session),
):
    user = await service.update_user(user_id, update_data, session)
    if not user:
        raise UserNotFound()
    return user


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_role_checker],
)
async def delete_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_user(user_id, session)
    if not deleted:
        raise UserNotFound()
    return {}
