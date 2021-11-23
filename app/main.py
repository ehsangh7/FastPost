
from fastapi import FastAPI
from . import models, database
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# with alembic dont need it
# models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# READ
@app.get("/")
async def root():
    return {"message": "Hello, world!"}


