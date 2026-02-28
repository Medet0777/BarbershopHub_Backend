from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
import uuid

from src.barbershops import service
from src.barbershops.schemas import BarbershopOut, BarbershopCreate, BarbershopUpdate
from src.dependencies import PaginationDependency, verify_admin_role

barbershop_router = APIRouter()


@barbershop_router.get(
    "/",
    response_model=List[BarbershopOut]
)
async def get_barbershops(
        pagination: PaginationDependency
):
    return service.get_all_barbershops(skip=pagination["skip"], limit=pagination["limit"])


@barbershop_router.get(
    "/{shop_id}",
    response_model=BarbershopOut
)
async def get_barbershop(shop_id: uuid.UUID):
    shop = service.get_barbershop_by_id(shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return shop


@barbershop_router.post(
    "/",
    response_model=BarbershopOut,
    status_code=status.HTTP_201_CREATED
)
async def create_barbershop(shop_data: BarbershopCreate):
    return service.create_barbershop(shop_data)


@barbershop_router.patch(
    "/{shop_id}",
    response_model=BarbershopOut
)
async def update_barbershop(shop_id: uuid.UUID, update_data: BarbershopUpdate):
    shop = service.update_barbershop(shop_id, update_data)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return shop


@barbershop_router.delete(
    "/{shop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_admin_role)]
)
async def delete_barbershop(shop_id: uuid.UUID):
    if not service.delete_barbershop(shop_id):
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return {}
