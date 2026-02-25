from fastapi import FastAPI

version = 'v1'

app = FastAPI(
    title="BBS",
    description="Barbershop booking system",
    version=version,
)

@app.get("/")
def root():
    return {"message": "Barbershop Booking System"}
