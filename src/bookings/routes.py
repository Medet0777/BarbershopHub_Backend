from fastapi import APIRouter, status, HTTPException
from typing import List
import uuid

from src.bookings import service
from src.bookings.schemas import BookingOut, BookingCreate, BookingUpdate

booking_router = APIRouter(prefix="/bookings", tags=["bookings"])


@booking_router.get(
    "/",
    response_model=List[BookingOut]
)
async def get_bookings():
    return service.get_all_bookings()


@booking_router.get(
    "/{booking_id}",
    response_model=BookingOut
)
async def get_booking(booking_id: uuid.UUID):
    bk = service.get_booking_by_id(booking_id)
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bk


@booking_router.post(
    "/", response_model=BookingOut,
    status_code=status.HTTP_201_CREATED
)
async def create_booking(booking_data: BookingCreate):
    return service.create_booking(booking_data)


@booking_router.patch(
    "/{booking_id}",
    response_model=BookingOut
)
async def update_booking(
        booking_id: uuid.UUID,
        update_data: BookingUpdate
):
    bk = service.update_booking(booking_id, update_data)
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bk


@booking_router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_booking(booking_id: uuid.UUID):
    if not service.delete_booking(booking_id):
        raise HTTPException(status_code=404, detail="Booking not found")
    return {}
