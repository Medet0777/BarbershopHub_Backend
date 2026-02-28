import uuid
from datetime import datetime, timezone

barbershops = [
    {
        "uid": uuid.uuid4(),
        "name": "Classic Cuts",
        "address": "123 Main St, Almaty",
        "phone": "+7 700 123 4567",
        "email": "classiccuts@example.com",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "name": "Sharp Style",
        "address": "45 Auezov St, Almaty",
        "phone": "+7 701 987 6543",
        "email": "sharpstyle@example.com",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
]