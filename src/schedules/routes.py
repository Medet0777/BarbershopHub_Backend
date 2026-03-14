from fastapi import APIRouter, status, Depends
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency
from src.db.session import get_session
from src.schedules import service
from src.schedules.schemas import ScheduleOut, ScheduleCreate, ScheduleUpdate
from src.auth.dependencies import RoleChecker
from src.errors import ScheduleNotFound

schedule_router = APIRouter()
admin_or_staff_role_checker = Depends(RoleChecker(["admin", "barbershop_staff"]))


@schedule_router.get("/", response_model=List[ScheduleOut])
async def get_schedules(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session),
):
    return await service.get_all_schedules(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session
    )


@schedule_router.get("/{schedule_id}", response_model=ScheduleOut)
async def get_schedule(
        schedule_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    sched = await service.get_schedule_by_id(schedule_id, session)
    if not sched:
        raise ScheduleNotFound()
    return sched


@schedule_router.post(
    "/",
    response_model=ScheduleOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_or_staff_role_checker],
)
async def create_schedule(
        sched_data: ScheduleCreate,
        session: AsyncSession = Depends(get_session),
):
    return await service.create_schedule(sched_data, session)


@schedule_router.patch(
    "/{schedule_id}",
    response_model=ScheduleOut,
    dependencies=[admin_or_staff_role_checker],
)
async def update_schedule(
        schedule_id: uuid.UUID,
        update_data: ScheduleUpdate,
        session: AsyncSession = Depends(get_session),
):
    sched = await service.update_schedule(schedule_id, update_data, session)
    if not sched:
        raise ScheduleNotFound()
    return sched


@schedule_router.delete(
    "/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_or_staff_role_checker],
)
async def delete_schedule(
        schedule_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    deleted = await service.delete_schedule(schedule_id, session)
    if not deleted:
        raise ScheduleNotFound()
    return {}
