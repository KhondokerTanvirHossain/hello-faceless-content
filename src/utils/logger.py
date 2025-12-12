"""
Logging configuration using loguru.
Provides structured logging for the application.
"""
import sys
from pathlib import Path
from loguru import logger

from src.config.settings import settings


def setup_logger():
    """Configure loguru logger with appropriate settings."""
    # Remove default handler
    logger.remove()

    # Add console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # Add file handler for persistent logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="00:00",  # Rotate daily at midnight
        retention="30 days",  # Keep logs for 30 days
        compression="zip",  # Compress old logs
    )

    # Add error-specific log file
    logger.add(
        log_dir / "errors_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="00:00",
        retention="90 days",  # Keep error logs longer
        compression="zip",
    )

    logger.info("Logger initialized successfully")


# Initialize logger on import
setup_logger()


# Export logger for use in other modules
__all__ = ["logger"]
