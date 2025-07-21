import sqlite3

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

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

@app.get("/drinks")
def get_drinks():
    return []
