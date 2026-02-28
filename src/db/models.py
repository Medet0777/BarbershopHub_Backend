import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, timezone
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
