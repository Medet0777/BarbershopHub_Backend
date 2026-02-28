from contextlib import asynccontextmanager
from src.db.main import initdb

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
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
