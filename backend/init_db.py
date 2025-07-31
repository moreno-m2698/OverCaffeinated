import os
import sqlite3
from config import get_settings

settings = get_settings()

SCHEMA_PATH = "sql/schema.sql"
MOCK_DATA_PATH = "sql/mock_data.sql"
DB_PATH = settings.DEV_DB_PATH

def run_sql_file(conn: sqlite3.Connection, filepath: str):
    """Execute all SQL commands in a given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)

def rebuild_database():
    """Remove old DB and create a fresh one using schema and mock data."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Deleted existing database at '{DB_PATH}'")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    print("Running schema...")
    run_sql_file(conn, SCHEMA_PATH)

    print("Inserting mock data...")
    run_sql_file(conn, MOCK_DATA_PATH)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at '{DB_PATH}'")

if __name__ == "__main__":
    rebuild_database()