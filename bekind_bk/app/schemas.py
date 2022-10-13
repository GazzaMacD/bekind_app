from pydantic import BaseModel
from datetime import datetime
from typing import List

#  ===== Post Schemas ============
"""
Post Schemas
"""


class CreatePostSch(BaseModel):
    title: str
    content: str
    published: bool = False


class UpdatePostSch(BaseModel):
    title: str
    content: str
    published: bool


# Response Schema
class BasePostRespDataSch(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class CreatePostRespSch(BaseModel):
    data: BasePostRespDataSch


class PostsRespSch(BaseModel):
    data: List[BasePostRespDataSch]


class UpdatePostRespSch(BaseModel):
    data: BasePostRespDataSch


class SinglePostRespSch(BaseModel):
    data: BasePostRespDataSch


class DeletePostRespSch(BaseModel):
    data: str


"""
User Schemas
"""

# Create User
class CreateUserSch(BaseModel):
    email: str
    password: str
    name: str


class UserBaseRespSch(BaseModel):
    id: int
    email: str
    name: str
    created: datetime

    class Config:
        orm_mode = True


class CreateUserRespSch(BaseModel):
    data: UserBaseRespSch
