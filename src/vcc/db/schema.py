from __future__ import annotations


SCHEMA_VERSION = 7


class DatabaseSchema:
    """
    Responsible for creating and updating the VCC database schema.
    """

    @staticmethod
    def initialize(connection):

        cursor = connection.cursor()

        #
        # Metadata
        #

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metadata
            (
                key     TEXT PRIMARY KEY,
                value   TEXT NOT NULL
            )
            """
        )

        #
        # Games
        #

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

        #
        # Tinfoil versions
        #

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tinfoil_titles
            (
                title_id    TEXT PRIMARY KEY,

                name        TEXT NOT NULL,

                version     INTEGER NOT NULL,

                synced_at   TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_tinfoil_titleid
            ON tinfoil_titles(title_id)
            """
        )

        #
        # NEW
        # Complete TitleDB metadata
        #

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
            CREATE TABLE IF NOT EXISTS title_regions
            (
                title_id        TEXT PRIMARY KEY,
                region          TEXT NOT NULL,
                source_region   TEXT,
                countries       TEXT NOT NULL DEFAULT '[]',
                source_title_id TEXT NOT NULL,
                synced_at       TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_title_regions_region
            ON title_regions(region)
            """
        )

        #
        # Activity log
        #

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

        #
        # Schema version
        #

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

        connection.commit()
