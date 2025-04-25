from sqlalchemy.orm import Session
from . import models

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def create_post(db: Session, title: str, content: str):
    db_post = models.Post(title=title, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post