from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./db.sqlite"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a database session.

    No autocommit, the caller has to explicitly call db.commit().
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
