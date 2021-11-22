
from fastapi import FastAPI
from . import models, database
from .routers import post, user, auth, vote

# with alembic dont need it
# models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# READ
@app.get("/")
async def root():
    return {"message": "Hello, world!"}


