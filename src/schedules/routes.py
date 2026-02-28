from fastapi import APIRouter, status, HTTPException
from typing import List
import uuid

from src.schedules import service
from src.schedules.schemas import ScheduleOut, ScheduleCreate, ScheduleUpdate

schedule_router = APIRouter(prefix="/schedules", tags=["schedules"])


@schedule_router.get(
    "/",
    response_model=List[ScheduleOut]
)
async def get_schedules():
    return service.get_all_schedules()


@schedule_router.get(
    "/{schedule_id}",
    response_model=ScheduleOut
)
async def get_schedule(schedule_id: uuid.UUID):
    sched = service.get_schedule_by_id(schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return sched


@schedule_router.post(
    "/",
    response_model=ScheduleOut,
    status_code=status.HTTP_201_CREATED
)
async def create_schedule(sched_data: ScheduleCreate):
    return service.create_schedule(sched_data)


@schedule_router.patch(
    "/{schedule_id}",
    response_model=ScheduleOut
)
async def update_schedule(schedule_id: uuid.UUID, update_data: ScheduleUpdate):
    sched = service.update_schedule(schedule_id, update_data)
    if not sched:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return sched


@schedule_router.delete(
    "/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_schedule(schedule_id: uuid.UUID):
    if not service.delete_schedule(schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {}
