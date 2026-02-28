import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException

from src.dependencies import PaginationDependency
from src.services import service
from src.services.schemas import ServiceOut, ServiceCreate, ServiceUpdate

service_router = APIRouter()


@service_router.get(
    "/",
    response_model=List[ServiceOut]
)
async def get_services(
        pagination: PaginationDependency
):
    return service.get_all_services(skip=pagination["skip"], limit=pagination["limit"])


@service_router.get(
    "/{service_id}",
    response_model=ServiceOut
)
async def get_service(service_id: uuid.UUID):
    srvc = service.get_service_by_id(service_id)
    if not srvc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    return srvc


@service_router.post(
    "/",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED
)
async def create_service(svc_data: ServiceCreate):
    return service.create_service(svc_data)


@service_router.patch(
    "/{service_id}",
    response_model=ServiceOut
)
async def update_service(service_id: uuid.UUID, update_data: ServiceUpdate):
    svc = service.update_service(service_id, update_data)
    if not svc:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )
    return svc


@service_router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(service_id: uuid.UUID):
    if not service.delete_service(service_id):
        raise HTTPException(
            status_code=404,
            detail="Service not found")
    return {}
