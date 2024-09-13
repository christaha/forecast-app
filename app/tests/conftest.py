import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base
from app.db import db_url, get_db
from app.main import app

engine = create_engine(db_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def session():
    session = TestingSessionLocal(bind=engine)
    yield session
    session.close()
