import uuid
from typing import List, Optional

from sqlmodel import select, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Review, Booking
from src.reviews.schemas import ReviewCreate, ReviewUpdate
from fastapi import HTTPException, status
from src.errors import DuplicateReview


async def get_all_reviews(skip: int = 0, limit: int = 100, session: AsyncSession = None, sort_by: str = "created_at", order: str = "desc", rating: int = None) -> List[Review]:
    statement = select(Review)
    if rating:
        statement = statement.where(Review.rating == rating)
    order_func = desc if order == "desc" else asc
    if hasattr(Review, sort_by):
        statement = statement.order_by(order_func(getattr(Review, sort_by)))
    statement = statement.offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


async def get_review_by_id(review_id: uuid.UUID, session: AsyncSession) -> Optional[Review]:
    result = await session.execute(
        select(Review).where(Review.uid == review_id)
    )
    return result.scalar_one_or_none()


async def get_reviews_by_barbershop(barbershop_id: uuid.UUID, session: AsyncSession) -> List[Review]:
    result = await session.execute(
        select(Review).where(Review.barbershop_id == barbershop_id)
    )
    return list(result.scalars().all())


async def get_review_by_booking(booking_id: uuid.UUID, session: AsyncSession) -> Optional[Review]:
    result = await session.execute(
        select(Review).where(Review.booking_id == booking_id)
    )
    return result.scalar_one_or_none()


async def create_review(review_data: ReviewCreate, user_id: uuid.UUID, session: AsyncSession) -> Review:
    # Check booking exists
    booking_result = await session.execute(select(Booking).where(Booking.uid == review_data.booking_id))
    booking = booking_result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    # Booking must be completed
    if booking.status != "Completed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can only review a completed booking")

    # Booking must belong to this user
    if booking.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only review your own bookings")

    # Check no duplicate review for this booking
    existing = await get_review_by_booking(review_data.booking_id, session)
    if existing:
        raise DuplicateReview()

    new_review = Review(
        user_id=user_id,
        barbershop_id=review_data.barbershop_id,
        booking_id=review_data.booking_id,
        rating=review_data.rating,
        comment=review_data.comment,
    )
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review


async def update_review(review_id: uuid.UUID, update_data: ReviewUpdate, session: AsyncSession) -> Optional[Review]:
    review = await get_review_by_id(review_id, session)
    if not review:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(review, key, value)
    await session.commit()
    await session.refresh(review)
    return review


async def delete_review(review_id: uuid.UUID, session: AsyncSession) -> bool:
    review = await get_review_by_id(review_id, session)
    if not review:
        return False
    await session.delete(review)
    await session.commit()
    return True
