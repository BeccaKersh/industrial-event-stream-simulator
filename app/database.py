import sqlite3

DATABASE_NAME = "industrial_events.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS machine_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            state TEXT NOT NULL,
            part_count INTEGER NOT NULL DEFAULT 0,
            downtime_reason TEXT
        )
        """
    )

    conn.commit()
    conn.close()