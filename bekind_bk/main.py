import random
import uuid
from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

db = {}

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


@app.post("/posts/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post, response: Response):
    post_id = uuid.uuid4()
    new_post = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "rating": post.rating,
    }
    db[post_id] = new_post
    return {"data": new_post}


@app.get("/posts/{id}")
async def get_post(id, response: Response):
    try:
        id = uuid.UUID(id)
        post = db[id]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid id parameter "
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this id does not exist",
        )
    return {"data": post}


@app.delete("/posts/{id}/delete")
async def delete_post(id, response: Response):
    try:
        id = uuid.UUID(id)
        post = db[id]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid id parameter "
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post with this id does not exist",
        )
    del db[id]
    return {"data": "post successfuly deleted"}
