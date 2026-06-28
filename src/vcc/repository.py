"""
VCC - Repository

High level database queries.
"""

from __future__ import annotations

from .database import Database


class Repository:
    
    def statistics(self):

        return {

            "games": self.total_game_files(),

            "base_games": self.total_base_games(),

            "updates": self.total_updates(),

            "orphan_updates": len(self.orphan_updates()),

            "duplicate_updates": len(self.duplicate_updates()),
        }
    
    def __init__(self, database: Database):

        self.database = database

    # -------------------------------------------------------------

    def total_game_files(self) -> int:

        cursor = self.database.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            """
        )

        return cursor.fetchone()[0]

    # -------------------------------------------------------------

    def total_base_games(self) -> int:

        cursor = self.database.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type='BASE'
            """
        )

        return cursor.fetchone()[0]

    # -------------------------------------------------------------

    def total_updates(self) -> int:

        cursor = self.database.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type='UPDATE'
            """
        )

        return cursor.fetchone()[0]

    # -------------------------------------------------------------

    def largest_games(self, limit: int = 10):

        cursor = self.database.connection.execute(
            """
            SELECT
                name,
                version,
                size,
                file_type
            FROM games
            ORDER BY size DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()

    # -------------------------------------------------------------

    def all_games(self):

        """
        Returns one record per BASE game with the
        highest installed update version.
        """

        cursor = self.database.connection.execute(
            """
            SELECT

                b.title_id,

                b.name,

                COALESCE(
                    MAX(u.version),
                    0
                ) AS installed_version

            FROM games b

            LEFT JOIN games u

                ON u.title_id =
                    substr(b.title_id,1,13) || '800'

                AND u.file_type='UPDATE'

            WHERE b.file_type='BASE'

            GROUP BY
                b.title_id,
                b.name

            ORDER BY
                b.name
            """
        )

        return cursor.fetchall()

        # -------------------------------------------------------------

    def games_with_latest_versions(self):

        """
        Returns all installed base games together with the
        latest version available on Tinfoil.
        """

        cursor = self.database.connection.execute(
            """
            SELECT

                b.title_id,

                b.name,

                COALESCE(
                    MAX(u.version),
                    0
                ) AS installed_version,

                COALESCE(
                    t.version,
                    0
                ) AS latest_version

            FROM games b

            LEFT JOIN games u

                ON u.title_id =
                    substr(b.title_id,1,13) || '800'

                AND u.file_type='UPDATE'

            LEFT JOIN tinfoil_titles t

                ON t.title_id = b.title_id

            WHERE
                b.file_type='BASE'

            GROUP BY
                b.title_id,
                b.name,
                t.version

            ORDER BY
                b.name
            """
        )

        return cursor.fetchall()
    
    # -------------------------------------------------------------

    def orphan_updates(self):

        cursor = self.database.connection.execute(
            """
            SELECT
                *
            FROM games
            WHERE
                file_type='UPDATE'

                AND substr(title_id,1,13) || '000'
                    NOT IN
                (
                    SELECT title_id
                    FROM games
                    WHERE file_type='BASE'
                )

            ORDER BY name
            """
        )

        return cursor.fetchall()

    # -------------------------------------------------------------

    def duplicate_updates(self):

        cursor = self.database.connection.execute(
            """
            SELECT

                title_id,

                version,

                COUNT(*) AS duplicates

            FROM games

            WHERE file_type='UPDATE'

            GROUP BY
                title_id,
                version

            HAVING COUNT(*) > 1

            ORDER BY title_id
            """
        )

        return cursor.fetchall()
        
    def debug_title_ids(self):

        cursor = self.database.connection.execute(
            """
            SELECT
                b.title_id AS base_title_id,
                substr(b.title_id,1,13) || '800' AS update_title_id,
                t.title_id AS tinfoil_title_id,
                t.version
            FROM games b
            LEFT JOIN tinfoil_titles t
                ON t.title_id = b.title_id
            WHERE b.file_type='BASE'
            LIMIT 20
            """
        )

        return cursor.fetchall()