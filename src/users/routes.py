import uuid
from typing import List

from fastapi import APIRouter, status, HTTPException, Depends

from src.dependencies import PaginationDependency, verify_admin_role
from src.users import service
from src.users.schemas import UserCreate, UserOut, UserUpdate

user_router = APIRouter()


@user_router.get("/", response_model=List[UserOut])
async def get_users(
        pagination: PaginationDependency
):
    return service.get_all_users(skip=pagination["skip"], limit=pagination["limit"])


@user_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: uuid.UUID):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user_data: UserCreate):
    return service.create_user(user_data)


@user_router.patch(
    "/{user_id}",
    response_model=UserOut
)
async def update_user(user_id: uuid.UUID, update_data: UserUpdate):
    user = service.update_user(user_id, update_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_admin_role)]
)
async def delete_user(user_id: uuid.UUID):
    user = service.delete_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {}
