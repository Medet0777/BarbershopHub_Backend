from fastapi import APIRouter, status, Depends, Query
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings import service
from src.bookings.schemas import BookingOut, BookingCreate, BookingUpdate
from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.auth.dependencies import RoleChecker, get_current_user
from src.db.models import User
from src.errors import BookingNotFound

booking_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
client_role_checker = Depends(RoleChecker(["admin", "client"]))


@booking_router.get("/", response_model=List[BookingOut], dependencies=[admin_role_checker])
async def get_bookings(
        pagination: PaginationDependency,
        status_filter: str = Query(None, alias="status"),
        sort_by: str = Query("created_at"),
        order: str = Query("desc"),
        session: AsyncSession = Depends(get_session),
):
    return await service.get_all_bookings(skip=pagination["skip"], limit=pagination["limit"], session=session, status_filter=status_filter, sort_by=sort_by, order=order)


@booking_router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
        booking_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    bk = await service.get_booking_by_id(booking_id, session)
    if not bk:
        raise BookingNotFound()
    return bk


@booking_router.post(
    "/",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[client_role_checker],
)
async def create_booking(
        booking_data: BookingCreate,
        session: AsyncSession = Depends(get_session),
):
    return await service.create_booking(booking_data, session)


@booking_router.patch(
    "/{booking_id}",
    response_model=BookingOut,
    dependencies=[client_role_checker],
)
async def update_booking(
        booking_id: uuid.UUID,
        update_data: BookingUpdate,
        session: AsyncSession = Depends(get_session),
):
    bk = await service.update_booking(booking_id, update_data, session)
    if not bk:
        raise BookingNotFound()
    return bk


@booking_router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_role_checker],
)
async def delete_booking(
        booking_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_booking(booking_id, session)
    if not deleted:
        raise BookingNotFound()
    return {}
