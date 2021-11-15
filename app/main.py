
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schema, utils, database, auth
from sqlalchemy.orm import Session
from .routers import post, user

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()





    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastpost',
                                user='exsan', password='ehsan2404',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection successfull")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite charecter", "content": "I LOVE ZLATAN", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# READ
@app.get("/")
async def root():
    return {"message": "Hello, world!"}


