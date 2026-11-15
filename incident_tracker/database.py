import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT    NOT NULL,
    description      TEXT    NOT NULL,
    category         TEXT    NOT NULL
        CHECK (category IN ('hardware', 'software', 'network', 'access', 'other')),
    impact           INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 3),
    urgency          INTEGER NOT NULL CHECK (urgency BETWEEN 1 AND 3),
    priority         TEXT    NOT NULL CHECK (priority IN ('P1', 'P2', 'P3', 'P4')),
    status           TEXT    NOT NULL
        CHECK (status IN ('new', 'in_progress', 'on_hold', 'resolved', 'closed')),
    reporter         TEXT    NOT NULL,
    assignee         TEXT,
    created_at       TEXT    NOT NULL,
    updated_at       TEXT    NOT NULL,
    resolved_at      TEXT,
    resolution_notes TEXT
);
"""

def get_connection(path):
    """Open a SQLite connection. Rows can be read by column name."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    """Create the tables if they don't exist yet."""
    conn.executescript(SCHEMA)
    conn.commit()