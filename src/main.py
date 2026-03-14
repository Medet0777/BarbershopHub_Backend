from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.users.routes import user_router
from src.services.routes import service_router
from src.schedules.routes import schedule_router
from src.bookings.routes import booking_router
from src.barbershops.routes import barbershop_router

version = "v1"


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    print("Server stopping")


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
app.include_router(booking_router, prefix=f"/api/{version}/bookings", tags=["bookings"])
app.include_router(barbershop_router, prefix=f"/api/{version}/barbershops", tags=["barbershops"])
