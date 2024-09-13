from typing import Generator
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

db_url = URL.create(
    "postgresql+psycopg2",
    username=settings.pg_username,
    password=settings.pg_password,
    host=settings.pg_host,
    port=settings.pg_port,
    database=settings.pg_database,
)

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
