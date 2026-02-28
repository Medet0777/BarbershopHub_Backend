from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config

async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def initdb():
    """create a connection to our db"""

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        statement = text("select 'Hello World'")

        result = await conn.execute(statement)

        print(result.all())