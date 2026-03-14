import uuid
from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.services import service
from src.services.schemas import ServiceOut, ServiceCreate, ServiceUpdate
from src.auth.dependencies import RoleChecker
from src.errors import ServiceNotFound

service_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
admin_or_staff_role_checker = Depends(RoleChecker(["admin", "barbershop_staff"]))


@service_router.get("/", response_model=List[ServiceOut])
async def get_services(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session),
):
    services_list = await service.get_all_services(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session
    )
    return services_list


@service_router.get("/{service_id}", response_model=ServiceOut)
async def get_service(
        service_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    srvc = await service.get_service_by_id(service_id, session)
    if not srvc:
        raise ServiceNotFound()
    return srvc


@service_router.post(
    "/",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_or_staff_role_checker],
)
async def create_service(
        svc_data: ServiceCreate,
        session: AsyncSession = Depends(get_session),
):
    new_svc = await service.create_service(svc_data, session)
    return new_svc


@service_router.patch(
    "/{service_id}",
    response_model=ServiceOut,
    dependencies=[admin_or_staff_role_checker],
)
async def update_service(
        service_id: uuid.UUID,
        update_data: ServiceUpdate,
        session: AsyncSession = Depends(get_session),
):
    svc = await service.update_service(service_id, update_data, session)
    if not svc:
        raise ServiceNotFound()
    return svc


@service_router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_role_checker],
)
async def delete_service(
        service_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_service(service_id, session)
    if not deleted:
        raise ServiceNotFound()
    return {}
