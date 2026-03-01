import uuid
from datetime import datetime, timezone
from typing import Optional, List

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import ForeignKey, Integer, Time
from sqlmodel import SQLModel, Field, Column, Relationship

from src.db.enums import RoleEnum, BookingStatusEnum


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
    role: str = Field(default=RoleEnum.CLIENT)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )

    barbershops: List["Barbershop"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    schedules: List["Schedule"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    bookings: List["Booking"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.email}>"


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
    owner_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("users.uid"),
            nullable=False
        )
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )

    owner: Optional["User"] = Relationship(
        back_populates="barbershops",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    services: List["Service"] = Relationship(
        back_populates="barbershop",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    schedules: List["Schedule"] = Relationship(
        back_populates="barbershop",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


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
    barbershop_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("barbershops.uid"),
            nullable=False
        )
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )

    barbershop: Optional["Barbershop"] = Relationship(
        back_populates="services",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    bookings: List["Booking"] = Relationship(
        back_populates="service",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


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
    )
    barbershop_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("barbershops.uid"),
            nullable=False
        )
    )
    day_of_week: int = Field(sa_column=Column(Integer, nullable=False))
    start_time: str = Field(sa_column=Column(Time, nullable=False))
    end_time: str = Field(sa_column=Column(Time, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )

    user: Optional["User"] = Relationship(
        back_populates="schedules",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    barbershop: Optional["Barbershop"] = Relationship(
        back_populates="schedules",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    bookings: List["Booking"] = Relationship(
        back_populates="schedule",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


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
    status: str = Field(default=BookingStatusEnum.PENDING)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc),
                         onupdate=lambda: datetime.now(timezone.utc))
    )

    user: Optional["User"] = Relationship(
        back_populates="bookings",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    service: Optional["Service"] = Relationship(
        back_populates="bookings",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    schedule: Optional["Schedule"] = Relationship(
        back_populates="bookings",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
