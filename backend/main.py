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