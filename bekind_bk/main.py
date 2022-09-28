from gzip import BadGzipFile
import random
from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

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


@app.post("/posts/create")
async def root(post: Post):
    print(post)
    return {"message": f"message successfuly posted."}
