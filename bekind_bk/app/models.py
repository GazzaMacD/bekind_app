from sqlalchemy import Column, Integer, String, Text, Boolean
from .db import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
