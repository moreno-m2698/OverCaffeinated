
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from datetime import datetime, timedelta, date, time, timezone
import os
import sqlite3

from routers import user_router, drink_router

app = FastAPI()
app.include_router(user_router)


# Serve static assets (e.g. JS, CSS, images)
app.mount("/assets", StaticFiles(directory="static/dist/assets"), name="assets")

# Serve index.html at root
@app.get("/")
def read_index():
    return FileResponse("static/dist/index.html")

# uvicorn main:app --reload
# fastapi dev main.py

class Drink:
    def __init__(self, id: int, name: str, caffeine: int, date: str): # Might need to create a datetime parser
        self.id = id
        self.name = name
        self.caffeine = caffeine
        self.date = date

dt_yesterday = datetime.combine(date=date.today(), time=time(hour=0, minute=0, second=0, microsecond=0)) - timedelta(days=1)

#ISO date time: YYYY-MM-DDTHH:mm:ss.SSSZ
mockDrinkData = [
    { 'id': 1, "name": "Espresso", "caffeine": 80, "date": dt_yesterday.isoformat() },
    { 'id': 2, "name": "Latte", "caffeine": 100, "date": dt_yesterday.isoformat() },
    { 'id': 3, "name": "Cold Brew", "caffeine": 200, "date": dt_yesterday.isoformat() },
    { 'id': 4, "name": "Green Tea", "caffeine": 60, "date": dt_yesterday.isoformat() }
]

@app.get("/api/drinks")
def get_drinks():


    return mockDrinkData

class DrinkIn(BaseModel):
    name: str
    caffeine: int
    date: str

@app.post("/api/drinks")
def post_drink(drink: DrinkIn):
    mockDrinkData.append(drink)
    print(mockDrinkData)
    return drink
