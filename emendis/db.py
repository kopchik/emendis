from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
