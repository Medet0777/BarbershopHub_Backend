import uuid
from typing import List

from fastapi import APIRouter, status, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.reviews import service
from src.reviews.schemas import ReviewOut, ReviewCreate, ReviewUpdate
from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.auth.dependencies import RoleChecker, get_current_user
from src.db.models import User
from src.errors import ReviewNotFound, DuplicateReview, InsufficientPermission
from src.rate_limiter import limiter, DEFAULT_RATE_LIMIT, HOURLY_RATE_LIMIT, WRITE_RATE_LIMIT

review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
client_role_checker = Depends(RoleChecker(["admin", "client"]))


@review_router.get("/", response_model=List[ReviewOut])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_reviews(
        request: Request,
        pagination: PaginationDependency,
        rating: int = Query(None, ge=1, le=5),
        sort_by: str = Query("created_at"),
        order: str = Query("desc"),
        session: AsyncSession = Depends(get_session),
):
    return await service.get_all_reviews(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session,
        sort_by=sort_by,
        order=order,
        rating=rating,
    )


@review_router.get("/{review_id}", response_model=ReviewOut)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_review(
        request: Request,
        review_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    review = await service.get_review_by_id(review_id, session)
    if not review:
        raise ReviewNotFound()
    return review


@review_router.post(
    "/",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[client_role_checker],
)
@limiter.limit(WRITE_RATE_LIMIT)
async def create_review(
        request: Request,
        review_data: ReviewCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    existing_review = await service.get_review_by_booking(review_data.booking_id, session)
    if existing_review:
        raise DuplicateReview()

    return await service.create_review(review_data, current_user.uid, session)


@review_router.patch(
    "/{review_id}",
    response_model=ReviewOut,
    dependencies=[client_role_checker],
)
@limiter.limit(WRITE_RATE_LIMIT)
async def update_review(
        request: Request,
        review_id: uuid.UUID,
        update_data: ReviewUpdate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    review = await service.get_review_by_id(review_id, session)
    if not review:
        raise ReviewNotFound()

    if review.user_id != current_user.uid and current_user.role != "admin":
        raise InsufficientPermission()

    updated = await service.update_review(review_id, update_data, session)
    return updated


@review_router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit(WRITE_RATE_LIMIT)
async def delete_review(
        request: Request,
        review_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    review = await service.get_review_by_id(review_id, session)
    if not review:
        raise ReviewNotFound()

    if review.user_id != current_user.uid and current_user.role != "admin":
        raise InsufficientPermission()

    await service.delete_review(review_id, session)
    return {}
