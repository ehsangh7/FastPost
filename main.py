from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/posts")
def get_posts():
    return {"message": "get post"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}