import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"
    BARBERSHOP_STAFF = "barbershop_staff"


class BookingStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class PaymentStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    REFUNDED = "Refunded"


class PaymentMethodEnum(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
