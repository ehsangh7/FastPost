from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite charecter", "content": "I LOVE ZLATAN", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    return {"post_detail": post}


@app.get("/posts")
def get_posts():
    return {"message": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post.dict())
    return {"data": post_dict}

# title