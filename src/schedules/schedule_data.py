import uuid
from datetime import datetime, time, timezone
from src.users.users_data import users

barbers = [user for user in users if user["role"] == "barbershop_staff"]

schedules = [
    {
        "uid": uuid.uuid4(),
        "user_id": barbers[0]["uid"] if barbers else uuid.uuid4(),
        "day_of_week": 0,  # Monday
        "start_time": time(hour=9, minute=0),
        "end_time": time(hour=17, minute=0),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "user_id": barbers[0]["uid"] if barbers else uuid.uuid4(),
        "day_of_week": 2,  # Wednesday
        "start_time": time(hour=10, minute=0),
        "end_time": time(hour=18, minute=0),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "user_id": barbers[1]["uid"] if len(barbers) > 1 else uuid.uuid4(),
        "day_of_week": 1,  # Tuesday
        "start_time": time(hour=9, minute=30),
        "end_time": time(hour=16, minute=30),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "user_id": barbers[1]["uid"] if len(barbers) > 1 else uuid.uuid4(),
        "day_of_week": 4,  # Friday
        "start_time": time(hour=11, minute=0),
        "end_time": time(hour=19, minute=0),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
]
