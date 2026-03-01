from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings import service
from src.bookings.schemas import BookingOut, BookingCreate, BookingUpdate
from src.dependencies import PaginationDependency, verify_admin_role
from src.db.session import get_session

booking_router = APIRouter()


@booking_router.get("/", response_model=List[BookingOut])
async def get_bookings(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session)
):
    return await service.get_all_bookings(skip=pagination["skip"], limit=pagination["limit"], session=session)


@booking_router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
        booking_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    bk = await service.get_booking_by_id(booking_id, session)
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bk


@booking_router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
        booking_data: BookingCreate,
        session: AsyncSession = Depends(get_session)
):
    return await service.create_booking(booking_data, session)


@booking_router.patch("/{booking_id}", response_model=BookingOut)
async def update_booking(
        booking_id: uuid.UUID,
        update_data: BookingUpdate,
        session: AsyncSession = Depends(get_session)
):
    bk = await service.update_booking(booking_id, update_data, session)
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bk


@booking_router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT,
                       dependencies=[Depends(verify_admin_role)])
async def delete_booking(
        booking_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    deleted = await service.delete_booking(booking_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {}
