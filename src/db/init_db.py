from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
import src.db.models  # noqa
from src.config import Config

async_engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def init_db(engine: AsyncEngine = async_engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
