from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel

from datetime import datetime, timedelta, date, time, timezone
import math
import sqlite3
from typing import Annotated

router = APIRouter(
    prefix="/drinks"
)



class Drink(BaseModel):
    name: str
    caffeine: int
    date: datetime
    poster_id: int

class DrinkDbModel(Drink):
    id: int

dt_yesterday = datetime.combine(date=date.today(), time=time(hour=0, minute=0, second=0)) - timedelta(days=1)

#ISO date time: YYYY-MM-DDTHH:mm:ss.SSSZ
mock_drink_data = [
    { 'id': 1, "name": "Espresso", "caffeine": 80, "date": dt_yesterday.isoformat(timespec="seconds") },
    { 'id': 2, "name": "Latte", "caffeine": 100, "date": dt_yesterday.isoformat(timespec="seconds") },
    { 'id': 3, "name": "Cold Brew", "caffeine": 200, "date": dt_yesterday.isoformat(timespec="seconds") },
    { 'id': 4, "name": "Green Tea", "caffeine": 60, "date": dt_yesterday.isoformat(timespec="seconds") }
]

@router.get("/")
def get_drinks():
    return mock_drink_data

@router.post("/")
def post_drinks(post):
    mock_drink_data.append(post)

class Point:
    x: float
    y: float

@router.get("/data")
def get_graph_data():
    
    # Half-life in seconds
    HL = 6 * 60 * 60 
    # Reaction constant
    K = math.log(2) / HL

    get_current_caffeine = lambda c0, td: c0 * (math.e ** (-K * td))
    
    res = []
    caffeine = 200

    return