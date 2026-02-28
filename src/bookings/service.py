import uuid
from datetime import datetime, timezone
from typing import List, Optional

from src.bookings.bookings_data import bookings
from src.bookings.schemas import BookingCreate, BookingUpdate

def get_all_bookings() -> List[dict]:
    return bookings

def get_booking_by_id(booking_id: uuid.UUID) -> Optional[dict]:
    for booking in bookings:
        if booking["uid"] == booking_id:
            return booking
    return None

def create_booking(booking_data: BookingCreate) -> dict:
    new_booking = {
        "uid": uuid.uuid4(),
        "user_id": booking_data.user_id,
        "service_id": booking_data.service_id,
        "schedule_id": booking_data.schedule_id,
        "status": booking_data.status or "Pending",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    bookings.append(new_booking)
    return new_booking

def update_booking(booking_id: uuid.UUID, update_data: BookingUpdate) -> Optional[dict]:
    bk = get_booking_by_id(booking_id)
    if not bk:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        bk[key] = value
    bk["updated_at"] = datetime.now(timezone.utc)
    return bk

def delete_booking(booking_id: uuid.UUID) -> bool:
    bk = get_booking_by_id(booking_id)
    if not bk:
        return False
    bookings.remove(bk)
    return True