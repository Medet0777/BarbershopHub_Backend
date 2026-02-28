from contextlib import asynccontextmanager
from src.db.main import initdb

from fastapi import FastAPI

from src.schedules.routes import schedule_router
from src.services.routes import service_router
from src.users.routes import user_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await initdb()
    yield
    print("server is stopping")


version = 'v1'

app = FastAPI(
    title="BBS",
    description="Barbershop booking system",
    version=version,
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "Barbershop Booking System"}


app.include_router(user_router, prefix=f"/api/{version}/users", tags=["users"])
app.include_router(service_router, prefix=f"/api/{version}/services", tags=["services"])
app.include_router(schedule_router, prefix=f"/api/{version}/schedules", tags=["schedules"])
