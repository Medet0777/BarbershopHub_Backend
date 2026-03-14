from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.barbershops import service
from src.barbershops.schemas import BarbershopOut, BarbershopCreate, BarbershopUpdate
from src.services.schemas import ServiceOut
from src.schedules.schemas import ScheduleOut
from src.reviews.schemas import ReviewOut
from src.reviews import service as review_service
from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.auth.dependencies import RoleChecker

barbershop_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
admin_or_staff_role_checker = Depends(RoleChecker(["admin", "barbershop_staff"]))


@barbershop_router.get("/", response_model=List[BarbershopOut])
async def get_barbershops(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session),
):
    return await service.get_all_barbershops(skip=pagination["skip"], limit=pagination["limit"], session=session)


@barbershop_router.get("/{shop_id}", response_model=BarbershopOut)
async def get_barbershop(
        shop_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    shop = await service.get_barbershop_by_id(shop_id, session)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return shop


@barbershop_router.get("/{shop_id}/services", response_model=List[ServiceOut])
async def get_barbershop_services(
        shop_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    shop = await service.get_barbershop_by_id(shop_id, session)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return shop.services


@barbershop_router.get("/{shop_id}/schedules", response_model=List[ScheduleOut])
async def get_barbershop_schedules(
        shop_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    shop = await service.get_barbershop_by_id(shop_id, session)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return shop.schedules


@barbershop_router.get("/{shop_id}/reviews", response_model=List[ReviewOut])
async def get_barbershop_reviews(
        shop_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    shop = await service.get_barbershop_by_id(shop_id, session)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return await review_service.get_reviews_by_barbershop(shop_id, session)


@barbershop_router.post(
    "/",
    response_model=BarbershopOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_or_staff_role_checker],
)
async def create_barbershop(
        shop_data: BarbershopCreate,
        session: AsyncSession = Depends(get_session),
):
    return await service.create_barbershop(shop_data, session)


@barbershop_router.patch(
    "/{shop_id}",
    response_model=BarbershopOut,
    dependencies=[admin_or_staff_role_checker],
)
async def update_barbershop(
        shop_id: uuid.UUID,
        update_data: BarbershopUpdate,
        session: AsyncSession = Depends(get_session),
):
    shop = await service.update_barbershop(shop_id, update_data, session)
    if not shop:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return shop


@barbershop_router.delete(
    "/{shop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_role_checker],
)
async def delete_barbershop(
        shop_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_barbershop(shop_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Barbershop not found")
    return {}
