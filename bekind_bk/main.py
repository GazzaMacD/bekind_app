import random
import uuid
from typing import Optional

from fastapi import FastAPI, Response, status
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


@app.post("/posts/create")
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
    response.status_code = status.HTTP_201_CREATED
    return {"data": new_post}


@app.get("/posts/{uid}")
async def get_post(uid, response: Response):
    try:
        uid = uuid.UUID(uid)
        post = db[uid]
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Not a valid uid parameter "}
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post with this uuid does not exist"}
    return {"data": post}


@app.delete("/posts/{uid}/delete")
async def delete_post(uid, response: Response):
    try:
        uid = uuid.UUID(uid)
        del db[uid]
        return {"data": "post deleted"}
    except ValueError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Not a valid uid parameter "}
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Post with this uuid does not exist"}
