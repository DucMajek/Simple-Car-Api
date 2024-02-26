from fastapi import FastAPI, Depends
from mysql_connector import MySQLConnector
import models


app = FastAPI()
_mysql_connector = MySQLConnector()


@app.post('/cars', tags=["Add new car"])
async def cars(name: str, model: str):
    return _mysql_connector.insert_new_car(name, model)

@app.post("/rate", response_model=models.RateCar, tags=["Rate Car"])
async def rate_car(data: models.RateCar = Depends()):
    _mysql_connector.rate_car(data.model, data.choice.value)
    return {"model": data.model, "choice": data.choice}


@app.get('/cars', tags=["Cars average rate"])
async def average_rate_cars():
    return _mysql_connector.get_average_rate_cars()

@app.get('/popular', tags=["Popular cars"])
async def popular_cars():
    return _mysql_connector.get_popular_cars()


