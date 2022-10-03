from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.private.private import get_private

host = get_private("DB_HOST")
port = get_private("DB_PORT")
database = get_private("DB_NAME")
user = get_private("DB_USER")
password = get_private("DB_PWD")

DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
