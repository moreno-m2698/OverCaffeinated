from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel

from datetime import datetime, timedelta, date, time, timezone

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

dt_yesterday = datetime.combine(date=date.today(), time=time(hour=0, minute=0, second=0, microsecond=0)) - timedelta(days=1)

#ISO date time: YYYY-MM-DDTHH:mm:ss.SSSZ
mock_drink_data = [
    { 'id': 1, "name": "Espresso", "caffeine": 80, "date": dt_yesterday.isoformat() },
    { 'id': 2, "name": "Latte", "caffeine": 100, "date": dt_yesterday.isoformat() },
    { 'id': 3, "name": "Cold Brew", "caffeine": 200, "date": dt_yesterday.isoformat() },
    { 'id': 4, "name": "Green Tea", "caffeine": 60, "date": dt_yesterday.isoformat() }
]

@router.get("/")
def get_drinks():
    return mock_drink_data