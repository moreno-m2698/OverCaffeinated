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
    def __init__(self, id, name, caffeine, date):
        self.id = id
        self.name = name
        self.caffeine = caffeine
        self.date = date

@app.get("/api/drinks")
def get_drinks():
    today = datetime.date.today()
    dt_today = datetime.datetime.fromisoformat()

    #ISO date time: YYYY-MM-DDTHH:mm:ss.SSSZ
    # mockDrinkData = [
    #     { id: 1, "name": "Espresso", "caffeine": 80, "date": yesterday.toISOString() },
    #     { id: 2, "name": "Latte", caffeine: 100, date: yesterday.toISOString() },
    #     { id: 3, name: "Cold Brew", caffeine: 200, date: yesterday.toISOString() },
    # ]
    return []
