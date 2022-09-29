from gzip import BadGzipFile
import random
import uuid
from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

db = []

# Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


@app.get("/")
async def root():
    random_int = random.randint(0, 9)
    return {"random_int": f"{random_int}"}


@app.get("/posts/")
async def posts():
    return {"data": db}


@app.post("/posts/create")
async def root(post: Post):
    new_post = {
        "id": uuid.uuid4(),
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "rating": post.rating,
    }
    db.append(new_post)
    return {"data": new_post}
