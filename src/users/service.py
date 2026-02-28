import uuid
from typing import Optional, List

from src.users.schemas import UserCreate, UserUpdate
from datetime import datetime, timezone
from src.users.users_data import users


def get_all_users(
        skip: int = 0, limit: int = 100
) -> List[dict]:
    return users[skip: skip + limit]


def get_user_by_id(user_id: uuid.UUID) -> Optional[dict]:
    for user in users:
        if user["uid"] == user_id:
            return user
    return None


def create_user(user_data: UserCreate) -> dict:
    new_user = {
        "uid": uuid.uuid4(),
        "name": user_data.name,
        "email": user_data.email,
        "password": user_data.password,
        "role": user_data.role,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    users.append(new_user)
    return new_user


def update_user(user_id: uuid.UUID, update_data: UserUpdate) -> Optional[dict]:
    user = get_user_by_id(user_id)
    if not user:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        user[key] = value
    user["updated_at"] = datetime.now(timezone.utc)
    return user


def delete_user(user_id: uuid.UUID) -> bool:
    user = get_user_by_id(user_id)
    if not user:
        return False
    users.remove(user)
    return True
