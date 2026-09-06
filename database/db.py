import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception:
        logger.exception("Database operation failed")
        raise
    finally:
        db.close()