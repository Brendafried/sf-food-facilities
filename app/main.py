from fastapi import FastAPI
from .load_data import load_food_trucks
from .routers import foodtrucks

app = FastAPI(title="SF Mobile Food Facilities API")

@app.on_event("startup")
def startup_event():
    data = load_food_trucks()
    app.state.food_trucks = data

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(foodtrucks.router, prefix="/api", tags=["foodtrucks"])
