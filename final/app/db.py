from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Iterator

DATABASE_URL = "sqlite:///./smart_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()