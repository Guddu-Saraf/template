import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


TEST_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5433/fastapi_test_db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database.db import get_db
from database.models import Base

TEST_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5433/fastapi_test_db"

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()



