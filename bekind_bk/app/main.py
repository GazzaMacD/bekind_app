import random
import uuid

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Union, Optional

from app.private.private import get_private

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


app = FastAPI()

db = {}

# Pydantic Models
class NewPost(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


class PostUpdate(BaseModel):
    title: str
    content: str
    published: bool
    rating: Union[int, None]


# Path operations


@app.get("/")
async def root():
    """
    Home route with dummy data now
    """
    random_int = random.randint(0, 9)
    return {"random_int": f"{random_int}"}


@app.get("/posts/")
async def posts():
    """
    Get all posts, published or unpublished
    """
    return {"data": db}


@app.post("/posts/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: NewPost):
    """
    Create new single post using NewPost pydantic class validation and defaults
    """
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
async def get_post(id):
    """
    Get single post using id
    """
    try:
        id = uuid.UUID(id)
        post = db[id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with this id does not exist",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid id parameter "
        )
    return {"data": post}


@app.put("/posts/{id}/update")
async def update_post(id, post: PostUpdate):
    """
    Update single post using id and put data
    """
    post_dict = post.dict()
    try:
        id = uuid.UUID(id)
        orig_post = db.get(id, None)
        if orig_post is None:
            raise KeyError
        db[id] = post_dict
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with this id does not exist",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid id parameter "
        )
    return {"data": post_dict}


@app.delete("/posts/{id}/delete")
async def delete_post(id):
    """
    Delete single post using id
    """
    try:
        id = uuid.UUID(id)
        del db[id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post with this id does not exist",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid id parameter "
        )
    return {"data": "post successfuly deleted"}
