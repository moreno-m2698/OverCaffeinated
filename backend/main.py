from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import datetime
import os
import sqlite3


app = FastAPI()

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



@app.get("/api/drinks")
def get_drinks():

    dt_yesterday: datetime.datetime = datetime.combine(date=datetime.date.today(), time=datetime.time(hour=0, minute=0, second=0, microsecond=0)) - datetime.timedelta(days=1)

    #ISO date time: YYYY-MM-DDTHH:mm:ss.SSSZ
    mockDrinkData = [
        { 'id': 1, "name": "Espresso", "caffeine": 80, "date": dt_yesterday.isoformat() },
        { 'id': 2, "name": "Latte", "caffeine": 100, "date": dt_yesterday.isoformat() },
        { 'id': 3, "name": "Cold Brew", "caffeine": 200, "date": dt_yesterday.isoformat() },
    ]
    
    return mockDrinkData
