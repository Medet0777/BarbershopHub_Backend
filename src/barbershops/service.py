import uuid
from datetime import datetime, timezone
from typing import List, Optional

from src.barbershops.barbershops_data import barbershops
from src.barbershops.schemas import BarbershopCreate, BarbershopUpdate

def get_all_barbershops() -> List[dict]:
    return barbershops

def get_barbershop_by_id(shop_id: uuid.UUID) -> Optional[dict]:
    for shop in barbershops:
        if shop["uid"] == shop_id:
            return shop
    return None

def create_barbershop(shop_data: BarbershopCreate) -> dict:
    new_shop = {
        "uid": uuid.uuid4(),
        "name": shop_data.name,
        "address": shop_data.address,
        "phone": shop_data.phone,
        "email": shop_data.email,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    barbershops.append(new_shop)
    return new_shop

def update_barbershop(shop_id: uuid.UUID, update_data: BarbershopUpdate) -> Optional[dict]:
    shop = get_barbershop_by_id(shop_id)
    if not shop:
        return None
    for key, value in update_data.model_dump(exclude_unset=True).items():
        shop[key] = value
    shop["updated_at"] = datetime.now(timezone.utc)
    return shop

def delete_barbershop(shop_id: uuid.UUID) -> bool:
    shop = get_barbershop_by_id(shop_id)
    if not shop:
        return False
    barbershops.remove(shop)
    return True