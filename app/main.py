
from fastapi import FastAPI
from . import models, database
from .routers import post, user, auth

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# READ
@app.get("/")
async def root():
    return {"message": "Hello, world!"}


