from contextlib import asynccontextmanager
from fastapi import FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.errors import register_error_handlers
from src.middleware import register_middleware
from src.rate_limiter import limiter
from src.auth.routes import auth_router
from src.users.routes import user_router
from src.services.routes import service_router
from src.schedules.routes import schedule_router
from src.bookings.routes import booking_router
from src.barbershops.routes import barbershop_router
from src.reviews.routes import review_router
from src.payments.routes import payment_router

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


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

register_error_handlers(app)
register_middleware(app)


@app.get("/")
async def root():
    return {"message": "Barbershop Booking System"}


app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(user_router, prefix=f"/api/{version}/users", tags=["users"])
app.include_router(service_router, prefix=f"/api/{version}/services", tags=["services"])
app.include_router(schedule_router, prefix=f"/api/{version}/schedules", tags=["schedules"])
app.include_router(booking_router, prefix=f"/api/{version}/bookings", tags=["bookings"])
app.include_router(barbershop_router, prefix=f"/api/{version}/barbershops", tags=["barbershops"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(payment_router, prefix=f"/api/{version}/payments", tags=["payments"])
