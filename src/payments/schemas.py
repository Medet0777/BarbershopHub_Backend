import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.db.enums import PaymentStatusEnum, PaymentMethodEnum


class PaymentBase(BaseModel):
    booking_id: uuid.UUID
    amount: float = Field(gt=0)
    payment_method: PaymentMethodEnum = PaymentMethodEnum.CASH


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatusEnum] = None
    payment_method: Optional[PaymentMethodEnum] = None


class PaymentOut(PaymentBase):
    uid: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
