from __future__ import annotations


class TinfoilRepository:
    """
    Handles all database operations related to the
    tinfoil_titles table.
    """

    def __init__(self, connection):

        self.connection = connection

    # ---------------------------------------------------------

    def clear(self):

        self.connection.execute(
            """
            DELETE FROM tinfoil_titles
            """
        )

    # ---------------------------------------------------------

    def save(self, titles: dict):

        """
        Store the latest available version for every TitleID.
        """

        self.clear()

        rows = []

        for item in titles.values():

            rows.append(
                (
                    item["title_id"],
                    item["version"],
                    item.get("media_version"),
                    item["synced_at"],
                )
            )

        self.connection.executemany(
            """
            INSERT INTO tinfoil_titles
            (
                title_id,
                version,
                media_version,
                synced_at
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            rows,
        )

        self.connection.commit()

    # ---------------------------------------------------------

    def save_media_versions(self, versions: dict):

        """Store versions discovered from Tinfoil.media."""

        rows = [
            (version, title_id.upper())
            for title_id, version in versions.items()
            if version is not None
        ]

        if not rows:
            self.connection.commit()
            return

        self.connection.executemany(
            """
            UPDATE tinfoil_titles
            SET media_version = ?
            WHERE title_id = ?
            """,
            rows,
        )

        self.connection.commit()

    # ---------------------------------------------------------

    def latest_version(self, title_id: str):

        cursor = self.connection.execute(
            """
            SELECT
                MAX(version, COALESCE(media_version, 0)) AS version

            FROM tinfoil_titles

            WHERE title_id = ?
            """,
            (
                title_id.upper(),
            ),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row["version"]

    # ---------------------------------------------------------

    def get(self, title_id: str):

        cursor = self.connection.execute(
            """
            SELECT *

            FROM tinfoil_titles

            WHERE title_id = ?
            """,
            (
                title_id.upper(),
            ),
        )

        return cursor.fetchone()

    # ---------------------------------------------------------

    def count(self):

        cursor = self.connection.execute(
            """
            SELECT COUNT(*)

            FROM tinfoil_titles
            """
        )

        return cursor.fetchone()[0]