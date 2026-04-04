import uuid
from typing import List

from fastapi import APIRouter, status, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.users import service
from src.users.schemas import UserCreate, UserOut, UserUpdate
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import UserNotFound
from src.rate_limiter import limiter, DEFAULT_RATE_LIMIT, HOURLY_RATE_LIMIT, WRITE_RATE_LIMIT

user_router = APIRouter()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))


@user_router.get("/", response_model=List[UserOut], dependencies=[admin_role_checker])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_users(
        request: Request,
        pagination: PaginationDependency,
        search: str = Query(None, description="Search by name or email"),
        sort_by: str = Query("created_at", description="Sort by field"),
        order: str = Query("desc", description="asc or desc"),
        session: AsyncSession = Depends(get_session),
):
    users = await service.get_all_users(
        skip=pagination["skip"],
        limit=pagination["limit"],
        search=search,
        sort_by=sort_by,
        order=order,
        session=session,
    )
    return users


@user_router.get("/{user_id}", response_model=UserOut, dependencies=[admin_role_checker])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_user(
        request: Request,
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
@limiter.limit(WRITE_RATE_LIMIT)
async def update_user(
        request: Request,
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
@limiter.limit(WRITE_RATE_LIMIT)
async def delete_user(
        request: Request,
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_user(user_id, session)
    if not deleted:
        raise UserNotFound()
    return {}
