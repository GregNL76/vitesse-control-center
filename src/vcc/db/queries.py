from __future__ import annotations

from .connection import DatabaseConnection


class DatabaseQueries:
    """
    Read-only database queries.
    """

    def __init__(self, connection: DatabaseConnection):

        self.connection = connection

    # -------------------------------------------------------------

    def statistics(self):

        storage = self.storage_by_type()

        return {
            "games": self.total_base_games(),
            "updates": self.total_updates(),
            "dlcs": self.total_dlcs(),

            "games_size": storage["games"],
            "updates_size": storage["updates"],
            "dlcs_size": storage["dlcs"],

            "orphan_updates": len(self.orphan_updates()),
            "duplicate_updates": len(self.duplicate_updates()),
        }

    # -------------------------------------------------------------

    def total_game_files(self) -> int:

        cursor = self.connection.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            """
        )

        return cursor.fetchone()[0]

    # -------------------------------------------------------------

    def total_base_games(self) -> int:

        cursor = self.connection.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type='BASE'
            """
        )

        return cursor.fetchone()[0]

    # -------------------------------------------------------------

    def total_updates(self) -> int:

        cursor = self.connection.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type='UPDATE'
            """
        )

        return cursor.fetchone()[0]

    # -------------------------------------------------------------

    def all_updates(self):

        cursor = self.connection.connection.execute(
            """
            SELECT
                id,
                name,
                title_id,
                version,
                filename,
                full_path,
                size
            FROM games
            WHERE file_type = 'UPDATE'
            ORDER BY name, version DESC
            """
        )

        return cursor.fetchall()

    # -------------------------------------------------------------

    def dlcs(self):
        
        cursor = self.connection.connection.execute(
            """
            SELECT
                g.title_id,
                g.name,
                g.version,
                g.filename,
                g.size,
                g.full_path,
                COALESCE(r.region, 'UNKNOWN') AS region
            FROM games g
            LEFT JOIN title_regions r ON r.title_id = g.title_id
            WHERE g.file_type='DLC'
            ORDER BY g.name COLLATE NOCASE
            """
        )

        return cursor.fetchall()
    
    # -------------------------------------------------------------

    def total_dlcs(self) -> int:

        cursor = self.connection.connection.execute(
            """
            SELECT COUNT(*)
            FROM games
            WHERE file_type='DLC'
            """
        )

        return cursor.fetchone()[0]
        
    # -------------------------------------------------------------

    def storage_by_type(self) -> dict:
        cursor = self.connection.connection.execute(
            """
            SELECT
                file_type,
                COALESCE(SUM(size), 0) AS total_size
            FROM games
            WHERE file_type IN ('BASE', 'UPDATE', 'DLC')
            GROUP BY file_type
            """
        )

        result = {
            "games": 0,
            "updates": 0,
            "dlcs": 0,
        }

        for row in cursor.fetchall():
            if row["file_type"] == "BASE":
                result["games"] = row["total_size"]
            elif row["file_type"] == "UPDATE":
                result["updates"] = row["total_size"]
            elif row["file_type"] == "DLC":
                result["dlcs"] = row["total_size"]

        return result

    # -------------------------------------------------------------

    def total_storage(self) -> int:

        cursor = self.connection.connection.execute(
            """
            SELECT
                COALESCE(SUM(size), 0)
            FROM games
            """
        )

        return cursor.fetchone()[0]
        
        # -------------------------------------------------------------

    def largest_games(self, limit: int = 10):

        cursor = self.connection.connection.execute(
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

        cursor = self.connection.connection.execute(
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

        cursor = self.connection.connection.execute(
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
                ) AS latest_version,

                m.publisher,

                m.developer,

                m.release_date,

                m.rating,

                m.icon_url,

                m.banner_url,

                m.languages,

                m.categories,

                COALESCE(r.region, 'UNKNOWN') AS region,

                CASE

                    WHEN COALESCE(MAX(u.version),0) < COALESCE(t.version,0)

                    THEN 1

                    ELSE 0

                END AS update_available

            FROM games b

            LEFT JOIN games u

                ON u.title_id =
                    substr(b.title_id,1,13) || '800'

                AND u.file_type='UPDATE'

            LEFT JOIN title_metadata m

                ON m.title_id = b.title_id

            LEFT JOIN tinfoil_titles t

                ON t.title_id = b.title_id

            LEFT JOIN title_regions r

                ON r.title_id = b.title_id

            WHERE

                b.file_type='BASE'

            GROUP BY

                b.title_id,
                b.name,

                t.version,

                m.publisher,
                m.developer,
                m.release_date,
                m.rating,
                m.icon_url,
                m.banner_url,
                m.languages,
                m.categories,
                r.region

            ORDER BY

                b.name
            """
        )

        return cursor.fetchall()
        
         # -------------------------------------------------------------

    def orphan_updates(self):

        cursor = self.connection.connection.execute(
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
        cursor = self.connection.connection.execute(
            """
            SELECT
                g.title_id,
                MAX(g.name) AS name,
                COUNT(*) AS update_count,
                MAX(g.version) AS latest_version
            FROM games g
            WHERE g.file_type = 'UPDATE'
            GROUP BY g.title_id
            HAVING COUNT(*) > 1
            ORDER BY name COLLATE NOCASE
            """
        )

        return cursor.fetchall()

        # -----------------------------------------------------------------

    def updates_for_title(self, title_id):

        cursor = self.connection.connection.cursor()

        cursor.execute(
            """
            SELECT

                id,
                title_id,
                filename,
                full_path,
                version,
                size

            FROM games

            WHERE
                title_id = ?
                AND file_type = 'UPDATE'

            ORDER BY
                version DESC
            """,
            (title_id,),
        )

        return cursor.fetchall()
        
    # -------------------------------------------------------------

    def duplicate_update_files(self):

        cursor = self.connection.connection.execute(
            """
            SELECT
                *
            FROM games
            WHERE file_type='UPDATE'
                AND (name, title_id, version) IN (
                    SELECT
                        name,
                        title_id,
                        version
                    FROM games
                    WHERE file_type='UPDATE'
                    GROUP BY
                        name,
                        title_id,
                        version
                    HAVING COUNT(*) > 1
                )
            ORDER BY name, title_id, version
            """
        )

        return cursor.fetchall()

    # -------------------------------------------------------------

    def debug_title_ids(self):

        cursor = self.connection.connection.execute(
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
        
    # -----------------------------------------------------------------

    def missing_updates(self):

        """
        Return all installed base games that have a newer version
        available in Tinfoil.
        """

        cursor = self.connection.connection.execute(
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
                ) AS latest_version,

                m.publisher,

                m.icon_url,

                CASE

                    WHEN COALESCE(MAX(u.version),0)
                         < COALESCE(t.version,0)

                    THEN 1

                    ELSE 0

                END AS update_available

            FROM games b

            LEFT JOIN games u

                ON u.title_id =
                    substr(b.title_id,1,13) || '800'

                AND u.file_type='UPDATE'

            LEFT JOIN title_metadata m

                ON m.title_id = b.title_id

            LEFT JOIN tinfoil_titles t

                ON t.title_id = b.title_id

            WHERE

                b.file_type='BASE'

            GROUP BY

                b.title_id,
                b.name,

                t.version,

                m.publisher,
                m.icon_url

            HAVING

                update_available = 1

            ORDER BY

                b.name
            """
        )

        return cursor.fetchall()        
        
    # -------------------------------------------------------------

    def latest_additions(self, limit: int = 10):
        cursor = self.connection.connection.execute(
            """
            SELECT
                name,
                filename,
                size,
                file_type,
                created
            FROM games
            ORDER BY created DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()
