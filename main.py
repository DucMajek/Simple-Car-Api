from fastapi import FastAPI, Depends
from models import RateCar
from services import *


app = FastAPI()


@app.post('/cars', tags=["Add new car"])
async def cars(name: str, model: str):
    return insert_new_car(name, model)


@app.post("/rate", response_model=RateCar, tags=["Rate Car"])
async def rate_car(data: RateCar = Depends()):
    await rate_car(data.model, int(data.choice.value))
    return {"model": data.model, "choice": data.choice}


@app.get('/cars', tags=["Cars average rate"])
async def average_rate_cars():
    return get_average_rate_cars()


@app.get('/popular', tags=["Popular cars"])
async def popular_cars():
    return get_popular_cars()


