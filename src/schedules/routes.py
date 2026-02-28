from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import PaginationDependency, verify_admin_or_barbershop_staff_role
from src.db.session import get_session
from src.schedules import service
from src.schedules.schemas import ScheduleOut, ScheduleCreate, ScheduleUpdate

schedule_router = APIRouter()


@schedule_router.get("/", response_model=List[ScheduleOut])
async def get_schedules(
        pagination: PaginationDependency,
        session: AsyncSession = Depends(get_session)
):
    return await service.get_all_schedules(
        skip=pagination["skip"],
        limit=pagination["limit"],
        session=session
    )


@schedule_router.get("/{schedule_id}", response_model=ScheduleOut)
async def get_schedule(
        schedule_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    sched = await service.get_schedule_by_id(schedule_id, session)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return sched


@schedule_router.post(
    "/",
    response_model=ScheduleOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_admin_or_barbershop_staff_role)]
)
async def create_schedule(
        sched_data: ScheduleCreate,
        session: AsyncSession = Depends(get_session)
):
    return await service.create_schedule(sched_data, session)


@schedule_router.patch(
    "/{schedule_id}",
    response_model=ScheduleOut,
    dependencies=[Depends(verify_admin_or_barbershop_staff_role)]
)
async def update_schedule(
        schedule_id: uuid.UUID,
        update_data: ScheduleUpdate,
        session: AsyncSession = Depends(get_session)
):
    sched = await service.update_schedule(schedule_id, update_data, session)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return sched


@schedule_router.delete(
    "/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_admin_or_barbershop_staff_role)]
)
async def delete_schedule(
        schedule_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    deleted = await service.delete_schedule(schedule_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {}
