import sqlite3

DATABASE = "database.db"

VALID_SEVERITIES = ("Low", "Medium", "High", "Critical")

VALID_STATUSES = ("Open", "In Progress", "Resolved", "Closed")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT NOT NULL
                CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')),
            status TEXT NOT NULL DEFAULT 'Open'
                CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
            assigned_to TEXT,
            date_created TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()