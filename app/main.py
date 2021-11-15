from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)


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

# READ
@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/posts", response_model = List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model = schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"couldn't find post {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"couldn't find post {id}"}
    return post



# CREATE
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schema.Post)
def create_post(post: schema.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #ORM
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



# UPDATE
@app.put("/posts/{id}", response_model = schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()

    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")

    # conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")
    
    updated_post.update(post.dict(), synchronize_session=False)
    
    db.commit()

    return updated_post.first()



# DELETE 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()

    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")

    # conn.commit()

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} does not exists!!!")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

