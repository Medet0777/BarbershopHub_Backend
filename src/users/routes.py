import uuid
from typing import List

from fastapi import APIRouter, status, Depends, Query, Request, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.users import service
from src.users.schemas import UserCreate, UserOut, UserUpdate
from src.auth.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from src.db.models import User
from src.errors import UserNotFound
from src.celery_tasks import compress_and_store_image
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


@user_router.post("/upload-image")
@limiter.limit(WRITE_RATE_LIMIT)
async def upload_profile_image(
        request: Request,
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
):
    image_bytes = await file.read()

    compress_and_store_image.delay(str(current_user.uid), image_bytes)

    return JSONResponse(
        content={
            "message": "Image uploaded, compression in progress",
            "original_size_kb": round(len(image_bytes) / 1024, 1),
        },
        status_code=status.HTTP_200_OK,
    )
