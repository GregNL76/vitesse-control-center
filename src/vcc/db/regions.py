from __future__ import annotations

import json
from datetime import datetime, timezone


class RegionRepository:
    """Store and retrieve the resolved region for library Title IDs."""

    def __init__(self, connection):
        self.connection = connection

    def replace(self, records: dict[str, dict]):
        synced_at = datetime.now(timezone.utc).isoformat()
        rows = []

        for title_id, item in records.items():
            rows.append(
                (
                    title_id.upper(),
                    item.get("region", "UNKNOWN"),
                    item.get("source_region"),
                    json.dumps(item.get("countries", []), ensure_ascii=False),
                    item.get("source_title_id", title_id).upper(),
                    synced_at,
                )
            )

        with self.connection:
            self.connection.execute("DELETE FROM title_regions")
            self.connection.executemany(
                """
                INSERT INTO title_regions
                (
                    title_id,
                    region,
                    source_region,
                    countries,
                    source_title_id,
                    synced_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def as_map(self) -> dict[str, str]:
        cursor = self.connection.execute(
            "SELECT title_id, region FROM title_regions ORDER BY title_id"
        )
        return {row["title_id"]: row["region"] for row in cursor.fetchall()}

    def count(self) -> int:
        return self.connection.execute(
            "SELECT COUNT(*) FROM title_regions"
        ).fetchone()[0]

    def matched_count(self) -> int:
        return self.connection.execute(
            "SELECT COUNT(*) FROM title_regions WHERE region != 'UNKNOWN'"
        ).fetchone()[0]
