from fastapi import Query, Depends
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
