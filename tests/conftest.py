import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from emendis.db import get_db
from emendis.main import app
from emendis.models import Base

TEST_DB = "sqlite:///./db_test.sqlite"


client = TestClient(app)


@pytest.fixture(scope="session")
def session_class():
    engine = create_engine(
        TEST_DB,
        connect_args={"check_same_thread": False},
        echo=True,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    db.execute(text("DROP TABLE IF EXISTS sensor_data"))
    db.execute(text("DROP TABLE IF EXISTS alembic_version"))
    Base.metadata.create_all(bind=engine)
    yield SessionLocal


@pytest.fixture(scope="session", autouse=True)
def override_get_db(session_class):
    db = session_class()

    def test_get_db():
        try:
            # TODO: create a nested transaction and roll it back at the end of each test,
            # but that would require cooperation between `db` fixture and apps's `test_get_db`.
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = test_get_db


@pytest.fixture
def db():
    yield from app.dependency_overrides[get_db]()
