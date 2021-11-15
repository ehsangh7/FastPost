from datetime import datetime
from pydantic import BaseModel


# Pydantic Schema Model
class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    
    created_at: datetime

    class Config:
        orm_mode = True