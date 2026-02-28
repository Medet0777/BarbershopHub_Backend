import uuid
from datetime import datetime, timezone
from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import ForeignKey, Integer, Time
from sqlmodel import SQLModel, Field, Column


# User model part
class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    name: str
    email: str = Field(index=True, nullable=False, unique=True)
    password: str
    role: str = Field(default="client")  # client/barbershop_staff/(might be admin)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )

    def __repr__(self):
        return f"<User{self.email}>"


# Booking model part
class Booking(SQLModel, table=True):
    __tablename__ = "bookings"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("users.uid"),
            nullable=False
        )
    )

    service_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("services.uid"),
            nullable=False
        )
    )

    schedule_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("schedules.uid"),
            nullable=False
        )
    )

    status: str = Field(default="Pending")

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )


# Schedule model part
class Schedule(SQLModel, table=True):
    __tablename__ = "schedules"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("users.uid"),
            nullable=False
        )
    )  # barbers slots

    day_of_week: int = Field(sa_column=Column(Integer, nullable=False))  # 0=Monday, 6=Sunday
    start_time: str = Field(sa_column=Column(Time, nullable=False))
    end_time: str = Field(sa_column=Column(Time, nullable=False))

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )


# Service model part
class Service(SQLModel, table=True):
    __tablename__ = "services"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    name: str
    description: Optional[str] = None
    category: str
    duration_minutes: int = Field(default=30)
    price: float = Field(default=0)

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )


class Barbershop(SQLModel, table=True):
    __tablename__ = "barbershops"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )

    name: str
    address: str
    phone: str
    email: str

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )
