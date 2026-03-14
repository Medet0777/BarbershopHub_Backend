import uuid
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.payments import service
from src.payments.schemas import PaymentOut, PaymentCreate, PaymentUpdate
from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.auth.dependencies import RoleChecker, get_current_user
from src.db.models import User
from src.errors import PaymentNotFound, DuplicatePayment

payment_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
client_role_checker = Depends(RoleChecker(["admin", "client"]))


@payment_router.get("/", response_model=List[PaymentOut], dependencies=[admin_role_checker])
async def get_payments(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session),
):
    return await service.get_all_payments(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session,
    )


@payment_router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(
        payment_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    payment = await service.get_payment_by_id(payment_id, session)
    if not payment:
        raise PaymentNotFound()
    return payment


@payment_router.post(
    "/",
    response_model=PaymentOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[client_role_checker],
)
async def create_payment(
        payment_data: PaymentCreate,
        session: AsyncSession = Depends(get_session),
):
    existing_payment = await service.get_payment_by_booking(payment_data.booking_id, session)
    if existing_payment:
        raise DuplicatePayment()

    return await service.create_payment(payment_data, session)


@payment_router.patch(
    "/{payment_id}",
    response_model=PaymentOut,
    dependencies=[admin_role_checker],
)
async def update_payment(
        payment_id: uuid.UUID,
        update_data: PaymentUpdate,
        session: AsyncSession = Depends(get_session),
):
    payment = await service.update_payment(payment_id, update_data, session)
    if not payment:
        raise PaymentNotFound()
    return payment


@payment_router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_role_checker],
)
async def delete_payment(
        payment_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_payment(payment_id, session)
    if not deleted:
        raise PaymentNotFound()
    return {}
