import sqlite3

from fastapi import FastAPI

# Run using 'fastapi dev main.py'

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/drink")
def drinks():
    # TODO: will allow user to see there drinks/add new drinks
    return {"drinks": 0}

@app.get("/login")
def login():
    # TODO: will log user in
    return []

@app.get("/logout")
def logout():
    # TODO: will log user out
    return []

@app.get("/caffeine")
def caffeine():
    # TODO: Will give you current amount of caffeine
    return []