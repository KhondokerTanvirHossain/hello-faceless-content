#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables and optionally seeds initial data.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.database import init_db, get_db_info, engine
from src.config.settings import settings
from src.utils.logger import logger


def main():
    """Initialize the database."""
    print("=" * 60)
    print("Database Initialization Script")
    print("=" * 60)
    print()

    # Show database location
    print(f"Database URL: {settings.database_url}")
    print()

    # Create database file directory if it doesn't exist
    db_path = Path("data/database")
    db_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Database directory ensured: {db_path}")
    print()

    # Initialize database (create tables)
    print("Creating database tables...")
    try:
        init_db()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        logger.error(f"Database initialization failed: {e}")
        return 1

    print()

    # Show database info
    print("Database Information:")
    print("-" * 60)
    try:
        db_info = get_db_info()
        print(f"  Tables: {', '.join(db_info['tables'])}")
        print(f"  Total: {db_info['table_count']} tables")
    except Exception as e:
        print(f"  Error getting database info: {e}")

    print()
    print("=" * 60)
    print("Database initialization complete!")
    print()
    print("Next steps:")
    print("  1. Configure .env file with API keys")
    print("  2. Test the system with: python -m src.core.content.script_generator")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
