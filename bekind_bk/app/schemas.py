from pydantic import BaseModel

# Pydantic Models
class CreatePostSch(BaseModel):
    title: str
    content: str
    published: bool = False


class UpdatePostSch(BaseModel):
    title: str
    content: str
    published: bool
