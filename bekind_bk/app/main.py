import random
import uuid

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Union, Optional
from passlib.context import CryptContext

from app.private.private import get_private
from . import models
from .db import SessionLocal, engine, get_db
from .schemas import (
    CreatePostSch,
    UpdatePostSch,
    CreatePostRespSch,
    PostsRespSch,
    UpdatePostRespSch,
    DeletePostRespSch,
    SinglePostRespSch,
    CreateUserRespSch,
    CreateUserSch,
)

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"])


"""
try:
    conn = psycopg2.connect(
        host=get_private("DB_HOST"),
        port=get_private("DB_PORT"),
        database=get_private("DB_NAME"),
        user=get_private("DB_USER"),
        password=get_private("DB_PWD"),
        cursor_factory=RealDictCursor,
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    print(cur.fetchall())
except Exception as error:
    print("Error", error)
"""

app = FastAPI()


# Path operations


@app.get("/")
async def root():
    """
    Home route with dummy data now
    """
    random_int = random.randint(0, 9)
    return {"random_int": f"{random_int}"}


@app.get(
    "/posts/",
    response_model=PostsRespSch,
)
async def posts(db: Session = Depends(get_db)):
    """
    Get all posts, published or unpublished
    """
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post(
    "/posts/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreatePostRespSch,
)
async def create_post(post: CreatePostSch, db: Session = Depends(get_db)):
    """
    Create new single post using NewPost pydantic class validation and defaults
    """
    # post_id = uuid.uuid4()
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # new_post = {
    #     "id": post_id,
    #     "title": post.title,
    #     "content": post.content,
    #     "published": post.published,
    #     "rating": post.rating,
    # }
    # db[post_id] = new_post
    return {"data": new_post}


@app.get("/posts/{id}", response_model=SinglePostRespSch)
async def get_post(id: int, db: Session = Depends(get_db)):
    """
    Get single post using id
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with this id does not exist",
        )
    return {"data": post}


@app.put(
    "/posts/{id}/update",
    response_model=UpdatePostRespSch,
)
async def update_post(id: int, post: UpdatePostSch, db: Session = Depends(get_db)):
    """
    Update single post using id and put data
    """
    post_dict = post.dict()
    postQ = db.query(models.Post).filter(models.Post.id == id)
    target_post = postQ.first()
    if not postQ.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with this id does not exist",
        )
    postQ.update(post_dict, synchronize_session=False)
    db.commit()
    db.refresh(target_post)
    return {"data": target_post}


@app.delete(
    "/posts/{id}/delete",
    response_model=DeletePostRespSch,
)
async def delete_post(id: int, db: Session = Depends(get_db)):
    """
    Delete single post using id
    """
    postQ = db.query(models.Post).filter(models.Post.id == id)
    if not postQ.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with this id does not exist",
        )
    postQ.delete(synchronize_session=False)
    db.commit()
    return {"data": "post successfuly deleted"}


@app.post(
    "/users/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserRespSch,
)
async def create_user(user: CreateUserSch, db: Session = Depends(get_db)):
    """
    Create new user using pydantic class validation and defaults
    """
    hashed = pwd_context.hash(user.password)
    new_user = models.User(email=user.email, password=hashed, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}
