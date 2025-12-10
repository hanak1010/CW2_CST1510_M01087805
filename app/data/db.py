import sqlite3
from pathlib import Path
from typing import Union

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.

    """
    db_path = Path(db_path)

    # Make sure directory exist
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create connection
    conn = sqlite3.connect(str(db_path))

    # To enable foreign key in sql
    conn.execute('PRAGMA foreign_keys = ON;')

    return conn
