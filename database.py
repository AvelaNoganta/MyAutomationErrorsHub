import sqlite3

DB_NAME = "error_hub.db"


class Database:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def init_db():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_name TEXT NOT NULL,
                category_id INTEGER,
                tool_name TEXT,
                error_message TEXT,
                root_cause TEXT,
                solution TEXT,
                image_path TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        default_categories = [
            "API Errors",
            "UI Errors",
            "Database Errors",
            "Environment Issues"
        ]

        for category in default_categories:
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name) VALUES (?)",
                (category,)
            )

        conn.commit()
        conn.close()
