import uuid
from datetime import datetime, timezone
from src.users.users_data import users
from src.services.services_data import services
from src.schedules.schedules_data import schedules

bookings = [
    {
        "uid": uuid.uuid4(),
        "user_id": users[0]["uid"] if users else uuid.uuid4(),
        "service_id": services[0]["uid"] if services else uuid.uuid4(),
        "schedule_id": schedules[0]["uid"] if schedules else uuid.uuid4(),
        "status": "Pending",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "user_id": users[1]["uid"] if len(users) > 1 else uuid.uuid4(),
        "service_id": services[1]["uid"] if len(services) > 1 else uuid.uuid4(),
        "schedule_id": schedules[1]["uid"] if len(schedules) > 1 else uuid.uuid4(),
        "status": "Confirmed",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
]