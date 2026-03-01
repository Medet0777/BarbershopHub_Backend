import enum


class RoleEnum(str, enum):
    ADMIN = "admin"
    CLIENT = "client"
    BARBERSHOP_STAFF = "barbershop_staff"


class BookingStatusEnum(str, enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
