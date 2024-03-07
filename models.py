from pydantic import BaseModel
from enum import Enum


class Rate(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class RateCar(BaseModel):
    model: str
    choice: int