from pydantic import BaseModel
from datetime import datetime

#  ===== Post Schemas ============
class CreatePostSch(BaseModel):
    title: str
    content: str
    published: bool = False


class UpdatePostSch(BaseModel):
    title: str
    content: str
    published: bool


class CreatePostRespDataSch(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class CreatePostRespSch(BaseModel):
    data: CreatePostRespDataSch
