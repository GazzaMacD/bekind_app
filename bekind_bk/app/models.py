from http import server
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .db import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default="FALSE", nullable=False)
    created = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
