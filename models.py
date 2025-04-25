from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# Set up the FastAPI app
app = FastAPI()

# Database URL (using SQLite for simplicity)
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"  # Change this for other databases (PostgreSQL, etc.)

# Create the SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database model for a Blog Post
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

# Pydantic model for Post input validation (used in requests)
class PostCreate(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True

# Initialize the database tables (run this only once)
Base.metadata.create_all(bind=engine)

# CRUD functions for the Blog
def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate):
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Routes for the Blog API
@app.get("/", response_model=dict)
def read_root():
    return {"message": "Welcome to the FastAPI Blog App!"}

# Route to get a specific post by ID
@app.get("/posts/{post_id}", response_model=PostCreate)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# Route to get all posts, with pagination support
@app.get("/posts/", response_model=List[PostCreate])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts(db, skip=skip, limit=limit)
    return posts

# Route to create a new post
@app.post("/posts/", response_model=PostCreate)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)