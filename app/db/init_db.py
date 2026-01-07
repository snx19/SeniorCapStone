"""Database initialization script."""
import logging
from app.db.base import Base, engine
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")

