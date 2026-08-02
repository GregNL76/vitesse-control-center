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
from src.vcc.db.tinfoil import TinfoilRepository
from src.vcc.db.queries import DatabaseQueries

SCHEMA_VERSION = 5


class Database:

    def __init__(self, database_file: Path = DATABASE_FILE):

        DATA_DIR.mkdir(parents=True, exist_ok=True)

        self.database_file = Path(database_file)

        self.connection = sqlite3.connect(
            self.database_file,
            timeout=30,
            check_same_thread=False,
        )

        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")

        self.connection.row_factory = sqlite3.Row

        self.queries = DatabaseQueries(self)

        self.tinfoil = TinfoilRepository(
            self.connection
        )
        
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
            CREATE TABLE IF NOT EXISTS title_metadata
            (
                title_id            TEXT PRIMARY KEY,

                name                TEXT,

                publisher           TEXT,

                developer           TEXT,

                description         TEXT,

                intro               TEXT,

                release_date        INTEGER,

                categories          TEXT,

                languages           TEXT,

                players             INTEGER,

                rating              TEXT,

                rating_content      TEXT,

                icon_url            TEXT,

                banner_url          TEXT,

                rights_id           TEXT,

                is_demo             INTEGER,

                latest_update_id    TEXT,

                latest_version      INTEGER,

                synced_at           TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_title_metadata_name
            ON title_metadata(name)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_title_metadata_publisher
            ON title_metadata(publisher)
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activity_log
            (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT NOT NULL,
                event_type      TEXT NOT NULL,
                severity        TEXT NOT NULL,
                title           TEXT NOT NULL,
                message         TEXT NOT NULL,
                details_json    TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_activity_event_type
            ON activity_log(event_type)
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

    def clear_title_metadata(self):

        """
        Remove all stored TitleDB metadata.
        """

        self.connection.execute(
            "DELETE FROM title_metadata"
        )

    # -----------------------------------------------------------------

    def save_title_metadata(self, metadata: dict):

        """
        Store normalized TitleDB metadata.
        """

        import json
        from datetime import datetime

        self.clear_title_metadata()

        synced = datetime.utcnow().isoformat()

        rows = []

        for item in metadata.values():

            rows.append(

                (

                    item["title_id"],

                    item.get("name"),

                    item.get("publisher"),

                    item.get("developer"),

                    item.get("description"),

                    item.get("intro"),

                    item.get("release_date"),

                    json.dumps(
                        item.get("categories", []),
                        ensure_ascii=False,
                    ),

                    json.dumps(
                        item.get("languages", []),
                        ensure_ascii=False,
                    ),

                    item.get("players"),

                    item.get("rating"),

                    json.dumps(
                        item.get("rating_content", []),
                        ensure_ascii=False,
                    ),

                    item.get("icon_url"),

                    item.get("banner_url"),

                    item.get("rights_id"),

                    1 if item.get("is_demo") else 0,

                    item.get("latest_update_id"),

                    item.get("latest_version"),

                    synced,

                )

            )

        self.connection.executemany(
            """
            INSERT INTO title_metadata
            (
                title_id,
                name,
                publisher,
                developer,
                description,
                intro,
                release_date,
                categories,
                languages,
                players,
                rating,
                rating_content,
                icon_url,
                banner_url,
                rights_id,
                is_demo,
                latest_update_id,
                latest_version,
                synced_at
            )
            VALUES
            (
                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?
            )
            """,
            rows,
        )

        self.connection.commit()

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
        
        # ---------------------------------------------------------

    def save_tinfoil_titles(self, titles):

        """
        Temporary compatibility wrapper.

        Eventually callers should use:

            database.tinfoil.save(...)
        """

        self.tinfoil.save(titles)
        
    # -----------------------------------------------------------------

    def game_count(self) -> int:

        cursor = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type = 'BASE'
            """
        )

        return cursor.fetchone()[0]


    # -----------------------------------------------------------------

    def update_count(self) -> int:

        cursor = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type = 'UPDATE'
            """
        )

        return cursor.fetchone()[0]


    # -----------------------------------------------------------------

    def metadata_count(self) -> int:

        cursor = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM title_metadata
            """
        )

        return cursor.fetchone()[0]        