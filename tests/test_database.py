import sqlite3
import pytest

from incident_tracker.database import get_connection, init_db

@pytest.fixture
def conn():
    """A fresh in-memory database for each test."""
    connection = get_connection(":memory:")
    init_db(connection)
    yield connection
    connection.close()


def test_init_db_creates_incidents_table(conn):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'"
    ).fetchone()
    assert row is not None


def test_can_insert_and_read_an_incident(conn):
    conn.execute(
        """
            INSERT INTO incidents
                (title, description, category, impact, urgency, priority, status, reporter, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("Outlook won't open", "Crashes on start", "software", 2, 2, "P3", "new", "alice", "2026-11-15T09:00:00", "2026-11-15T09:00:00"),
    )
    row = conn.execute("SELECT * FROM incidents WHERE id = 1").fetchone()
    assert row["title"] == "Outlook won't open"
    assert row["status"] == "new"


def test_database_rejects_invalid_impact(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute (
            """
                INSERT INTO incidents
                    (title, description, category, impact, urgency, priority,
                    status, reporter, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("Bad", "Bad", "software", 5, 2, "P3",
             "new", "alice", "2026-11-15T09:00:00", "2026-11-15T09:00:00"),  
        )

def test_sql_injection_text_is_stored_as_plain_text(conn):
    nasty = "'; DROP TABLE incidents; --"
    conn.execute (
        """
            INSERT INTO incidents
                (title, description, category, impact, urgency, priority, status, reporter, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (nasty, "x", "other", 3, 3, "P4",
         "new", "mallory", "2026-11-15T09:00:00", "2026-11-15T09:00:00"),
    )
    row = conn.execute("SELECT title FROM incidents").fetchone()
    assert row["title"] == nasty