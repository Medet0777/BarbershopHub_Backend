from fastapi import Query, Depends, Header, HTTPException, status
from typing import Annotated


async def validate_limit(
        limit: int = Query(100, ge=1, le=100, description="Max number of items to return")
) -> int:
    MAX_LIMIT = 100
    return min(limit, MAX_LIMIT)


LimitSubDependency = Annotated[int, Depends(validate_limit)]


async def pagination(
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: LimitSubDependency = 100
):
    return {"skip": skip, "limit": limit}


PaginationDependency = Annotated[dict, Depends(pagination)]


async def verify_admin_role(
        x_role: str = Header(...)
):
    if x_role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )


async def verify_admin_or_barbershop_staff_role(
        x_role: str = Header(...)
):
    if x_role.lower() not in ["admin", "barbershop_staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Barbershop Staff privileges required"
        )


async def verify_admin_or_client_role(
        x_role: str = Header(...)
):
    if x_role.lower() not in ["admin", "client"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Client  privileges required"
        )
