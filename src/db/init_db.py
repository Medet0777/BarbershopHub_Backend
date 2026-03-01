from sqlmodel import SQLModel
from src.db.session import engine
import src.db.models  # noqa


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
