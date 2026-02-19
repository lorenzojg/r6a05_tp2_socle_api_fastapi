from __future__ import annotations
from typing import Generator
from sqlalchemy.orm import Session, sessionmaker

from app.db.engine import get_engine

def get_db() -> Generator[Session, None, None]:
    db = Session()
    try:
        yield db
    finally:
        db.close()