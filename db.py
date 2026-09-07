"""
db.py

The single place in the project that opens a connection to the SQLite database.

Every other file (seed.py, later app.py) calls get_connection() instead of
opening the database itself. That way the file path is written down once, and
every connection gets the same settings applied.
"""

import sqlite3
from pathlib import Path

# Path to the database file.
#
#   Path(__file__)          -> this file, db.py
#   .resolve().parent       -> the folder db.py lives in (the project root)
#   / "data" / "foodapp.db" -> the database file inside data/
#
# Anchoring to this file's location (rather than a plain "data/foodapp.db")
# means it doesn't matter which directory you run python from -- seed.py and
# flask run both point at the same file.
DB_PATH = Path(__file__).resolve().parent / "data" / "foodapp.db"


def get_connection():
    """Open a connection to the database and return it, ready to use.

    The caller is responsible for closing it (or using it in a `with` block).
    """
    # Open the connection. If the file doesn't exist yet, SQLite creates an
    # empty one -- which is what happens the first time seed.py runs.
    connection = sqlite3.connect(DB_PATH)

    # Make query results behave like dicts: row["name"] instead of row[0].
    # Accessing columns by name is much harder to get wrong than by number.
    connection.row_factory = sqlite3.Row

    # Turn on foreign-key enforcement. SQLite ignores REFERENCES clauses
    # unless this is set, and it must be set on every new connection -- which
    # is the main reason this function exists.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
