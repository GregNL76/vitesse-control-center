from __future__ import annotations

import json
from datetime import datetime


class MetadataStorage:
    """
    Store TitleDB metadata and Tinfoil version information.
    """

    def __init__(self, connection):

        self.connection = connection

    # ---------------------------------------------------------
    # Tinfoil versions
    # ---------------------------------------------------------

    def clear_tinfoil_titles(self):

        self.connection.connection.execute(
            "DELETE FROM tinfoil_titles"
        )

    def save_tinfoil_titles(
        self,
        titles: dict,
    ):

        self.clear_tinfoil_titles()

        synced = datetime.utcnow().isoformat()

        self.connection.connection.executemany(
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

    # ---------------------------------------------------------
    # Complete TitleDB metadata
    # ---------------------------------------------------------

    def clear_title_metadata(self):

        self.connection.connection.execute(
            "DELETE FROM title_metadata"
        )

    def save_title_metadata(
        self,
        metadata: dict[str, dict],
    ):

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

        self.connection.connection.executemany(
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