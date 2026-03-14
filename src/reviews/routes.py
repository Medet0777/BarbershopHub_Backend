import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.reviews import service
from src.reviews.schemas import ReviewOut, ReviewCreate, ReviewUpdate
from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.auth.dependencies import RoleChecker, get_current_user
from src.db.models import User

review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
client_role_checker = Depends(RoleChecker(["admin", "client"]))


@review_router.get("/", response_model=List[ReviewOut])
async def get_reviews(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session),
):
    return await service.get_all_reviews(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session,
    )


@review_router.get("/{review_id}", response_model=ReviewOut)
async def get_review(
        review_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    review = await service.get_review_by_id(review_id, session)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@review_router.post(
    "/",
    response_model=ReviewOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[client_role_checker],
)
async def create_review(
        review_data: ReviewCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    existing_review = await service.get_review_by_booking(review_data.booking_id, session)
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Review for this booking already exists",
        )

    return await service.create_review(review_data, current_user.uid, session)


@review_router.patch(
    "/{review_id}",
    response_model=ReviewOut,
    dependencies=[client_role_checker],
)
async def update_review(
        review_id: uuid.UUID,
        update_data: ReviewUpdate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    review = await service.get_review_by_id(review_id, session)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.uid and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only update your own reviews")

    updated = await service.update_review(review_id, update_data, session)
    return updated


@review_router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
        review_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    review = await service.get_review_by_id(review_id, session)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.uid and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only delete your own reviews")

    await service.delete_review(review_id, session)
    return {}
