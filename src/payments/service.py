import uuid
from typing import List, Optional

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Payment
from src.payments.schemas import PaymentCreate, PaymentUpdate


async def get_all_payments(skip: int = 0, limit: int = 100, session: AsyncSession = None) -> List[Payment]:
    result = await session.execute(
        select(Payment).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_payment_by_id(payment_id: uuid.UUID, session: AsyncSession) -> Optional[Payment]:
    result = await session.execute(
        select(Payment).where(Payment.uid == payment_id)
    )
    return result.scalar_one_or_none()


async def get_payment_by_booking(booking_id: uuid.UUID, session: AsyncSession) -> Optional[Payment]:
    result = await session.execute(
        select(Payment).where(Payment.booking_id == booking_id)
    )
    return result.scalar_one_or_none()


async def create_payment(payment_data: PaymentCreate, session: AsyncSession) -> Payment:
    new_payment = Payment(
        booking_id=payment_data.booking_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
    )
    session.add(new_payment)
    await session.commit()
    await session.refresh(new_payment)
    return new_payment


async def update_payment(payment_id: uuid.UUID, update_data: PaymentUpdate, session: AsyncSession) -> Optional[Payment]:
    payment = await get_payment_by_id(payment_id, session)
    if not payment:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(payment, key, value)
    await session.commit()
    await session.refresh(payment)
    return payment


async def delete_payment(payment_id: uuid.UUID, session: AsyncSession) -> bool:
    payment = await get_payment_by_id(payment_id, session)
    if not payment:
        return False
    await session.delete(payment)
    await session.commit()
    return True
