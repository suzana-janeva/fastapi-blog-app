from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    class Config:
        orm_mode = True