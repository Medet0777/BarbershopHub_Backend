import uuid
from datetime import datetime, timezone
from typing import List, Optional

from src.services.schemas import ServiceCreate, ServiceUpdate
from src.services.services_data import services


def get_all_services(
        skip: int = 0, limit: int = 100
) -> List[dict]:
    return services[skip: skip + limit]


def get_service_by_id(service_id: uuid.UUID) -> Optional[dict]:
    for service in services:
        if service["uid"] == service_id:
            return service
    return None


def create_service(service_data: ServiceCreate) -> dict:
    new_service = {
        "uid": uuid.uuid4(),
        "name": service_data.name,
        "description": service_data.description,
        "category": service_data.category,
        "duration_minutes": service_data.duration_minutes,
        "price": service_data.price,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    services.append(new_service)
    return new_service


def update_service(service_id: uuid.UUID, update_data: ServiceUpdate) -> Optional[dict]:
    service = get_service_by_id(service_id)
    if not service:
        return None

    for key, value in update_data.model_dump(exclude_unset=True).items():
        service[key] = value
    service["updated_at"] = datetime.now(timezone.utc)
    return service


def delete_service(service_id: uuid.UUID) -> bool:
    service = get_service_by_id(service_id)
    if not service:
        return False
    services.remove(service)
    return True
