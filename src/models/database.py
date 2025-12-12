"""
Database configuration and session management using SQLAlchemy.
"""
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from src.config.settings import settings
from src.utils.logger import logger


# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_session() -> Session:
    """
    Get a new database session.

    Returns:
        SQLAlchemy session

    Usage:
        session = get_session()
        try:
            # Do database operations
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    """
    return SessionLocal()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Automatically commits on success, rolls back on error, and closes session.

    Yields:
        SQLAlchemy session

    Usage:
        with get_db_session() as session:
            job = session.query(Job).filter_by(id=1).first()
            job.status = "completed"
            # Auto-commit on exit
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()


def init_db() -> None:
    """
    Create all database tables.
    Call this during initial setup.
    """
    logger.info("Initializing database...")

    # Import all models so they're registered with Base
    from src.models.job import Job
    from src.models.content import Script
    from src.models.approval import Approval

    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")


def drop_all_tables() -> None:
    """
    Drop all database tables.
    WARNING: This will delete all data!
    Use only for testing or database reset.
    """
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped")


def get_db_info() -> dict:
    """
    Get information about the database.

    Returns:
        Dictionary with database info
    """
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    return {
        "database_url": settings.database_url,
        "tables": tables,
        "table_count": len(tables),
    }
