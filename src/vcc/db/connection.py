from __future__ import annotations

import sqlite3
from pathlib import Path


class DatabaseConnection:
    """
    Simple wrapper around a SQLite connection.
    """

    def __init__(self, database_path: str | Path):

        self.database_path = Path(database_path)

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

    def execute(self, *args, **kwargs):

        return self.connection.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):

        return self.connection.executemany(*args, **kwargs)

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    def close(self):

        self.connection.close()

    def cursor(self):

        return self.connection.cursor()