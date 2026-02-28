from fastapi import Query, Depends
from typing import Annotated


async def pagination(
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(100, ge=1, le=100, description="Max number of items to return")
):
    return {"skip": skip, "limit": limit}


PaginationDependency = Annotated[dict, Depends(pagination)]
