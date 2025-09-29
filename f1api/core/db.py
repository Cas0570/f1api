from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from f1api.core.config import settings

# Engine (sync, SQLAlchemy 2.x)
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Handy context-managed session (optional usage later)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
