"""
VCC - SQLite database

Responsible for creating and maintaining the VCC database.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import DATA_DIR, DATABASE_FILE
from .game import GameFile
from .library import Library

SCHEMA_VERSION = 2


class Database:

    def __init__(self, database_file: Path = DATABASE_FILE):

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        self.database_file = Path(database_file)

        self.connection = sqlite3.connect(self.database_file)

        self.connection.row_factory = sqlite3.Row

    # -----------------------------------------------------------------

    def close(self):

        self.connection.close()

    # -----------------------------------------------------------------

    def initialize(self):

        """
        Create database schema if it does not yet exist.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata
            (
                key     TEXT PRIMARY KEY,
                value   TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS games
            (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,

                title_id        TEXT NOT NULL,
                name            TEXT NOT NULL,

                version         INTEGER NOT NULL,

                file_type       TEXT NOT NULL,

                filename        TEXT NOT NULL,

                full_path       TEXT NOT NULL UNIQUE,

                size            INTEGER NOT NULL,

                created         TEXT,

                modified        TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_titleid
            ON games(title_id)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_name
            ON games(name)
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tinfoil_titles
            (
                title_id        TEXT PRIMARY KEY,

                name            TEXT NOT NULL,

                version         INTEGER NOT NULL,

                synced_at       TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_tinfoil_titleid
            ON tinfoil_titles(title_id)
            """
        )

        cursor.execute(
            """
            INSERT OR REPLACE INTO metadata
            (
                key,
                value
            )
            VALUES
            (
                'schema_version',
                ?
            )
            """,
            (str(SCHEMA_VERSION),),
        )

        self.connection.commit()

    # -----------------------------------------------------------------

    @property
    def schema_version(self) -> int:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT value
            FROM metadata
            WHERE key='schema_version'
            """
        )

        row = cursor.fetchone()

        if row is None:
            return 0

        return int(row["value"])

    # -----------------------------------------------------------------

    def clear_games(self):

        """
        Remove all stored game records.
        """

        self.connection.execute(
            "DELETE FROM games"
        )


    # -----------------------------------------------------------------

    def clear_tinfoil_titles(self):

        """
        Remove all Tinfoil titles.
        """

        self.connection.execute(
            "DELETE FROM tinfoil_titles"
        )

    # -----------------------------------------------------------------

    def insert_game_file(
        self,
        name: str,
        game_file: GameFile,
    ):

        self.connection.execute(
            """
            INSERT OR REPLACE INTO games
            (
                title_id,
                name,
                version,
                file_type,
                filename,
                full_path,
                size,
                created,
                modified
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?
            )
            """,
            (
                game_file.title_id,
                name,
                game_file.version,
                game_file.file_type,
                game_file.filename,
                str(game_file.path),
                game_file.size,
                game_file.created.isoformat() if game_file.created else None,
                game_file.modified.isoformat() if game_file.modified else None,
            ),
        )

    # -----------------------------------------------------------------

    def save_library(self, library: Library):

        """
        Replace database contents with the current scan.
        """

        self.clear_games()

        for game in library.all_games():

            if game.base:

                self.insert_game_file(
                    game.name,
                    game.base,
                )

            for update in game.updates:

                self.insert_game_file(
                    game.name,
                    update,
                )

        self.connection.commit()

    # -----------------------------------------------------------------

    def save_tinfoil_titles(self, titles: dict):

        """
        Store the complete Tinfoil title database.
        """

        from datetime import datetime

        self.clear_tinfoil_titles()

        synced = datetime.utcnow().isoformat()

        self.connection.executemany(
            """
            INSERT INTO tinfoil_titles
            (
                title_id,
                name,
                version,
                synced_at
            )
            VALUES
            (
                ?,?,?,?
            )
            """,
            [
                (
                    item["title_id"],
                    item["name"],
                    item["version"],
                    synced,
                )
                for item in titles.values()
            ],
        )

        self.connection.commit()

    # -----------------------------------------------------------------

    def stats(self) -> dict:

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM games
            """
        )

        game_files = cursor.fetchone()[0]
        
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tinfoil_titles
            """
        )

        tinfoil_titles = cursor.fetchone()[0]

        return {
            "database": str(self.database_file),
            "schema": self.schema_version,
            "game_files": game_files,
            "tinfoil_titles": tinfoil_titles,
        }