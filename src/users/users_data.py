import uuid
from datetime import datetime, timezone

users = [
    {
        "uid": uuid.uuid4(),
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "password": "password123",  # hash will be later
        "role": "client",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "name": "Bob Smith",
        "email": "bob@example.com",
        "password": "password123",
        "role": "barbershop_staff",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "password": "password123",
        "role": "client",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "name": "David Lee",
        "email": "david@example.com",
        "password": "password123",
        "role": "barbershop_staff",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "uid": uuid.uuid4(),
        "name": "Eve Martinez",
        "email": "eve@example.com",
        "password": "password123",
        "role": "client",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
]
