from __future__ import annotations

import json
from datetime import datetime


class ActivityStorage:
    """
    Store and retrieve activity log entries.
    """

    def __init__(self, connection):

        self.connection = connection

    # ---------------------------------------------------------
    # Add activity
    # ---------------------------------------------------------

    def add(
        self,
        event_type: str,
        severity: str,
        title: str,
        message: str,
        details_json=None,
        timestamp: str | None = None,
    ):

        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()

        if (
            details_json is not None
            and not isinstance(details_json, str)
        ):
            details_json = json.dumps(
                details_json,
                ensure_ascii=False,
            )

        self.connection.connection.execute(
            """
            INSERT INTO activity_log
            (
                timestamp,
                event_type,
                severity,
                title,
                message,
                details_json
            )
            VALUES
            (
                ?,?,?,?,?,?
            )
            """,
            (
                timestamp,
                event_type,
                severity,
                title,
                message,
                details_json,
            ),
        )

        self.connection.commit()

    # ---------------------------------------------------------
    # Recent activity
    # ---------------------------------------------------------

    def recent(
        self,
        limit: int = 5,
    ):

        cursor = self.connection.connection.execute(
            """
            SELECT

                id,

                timestamp,

                event_type,

                severity,

                title,

                message,

                details_json

            FROM activity_log

            ORDER BY timestamp DESC

            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()

    # ---------------------------------------------------------
    # Last event
    # ---------------------------------------------------------

    def last(
        self,
        event_type: str,
    ):

        cursor = self.connection.connection.execute(
            """
            SELECT

                id,

                timestamp,

                event_type,

                severity,

                title,

                message,

                details_json

            FROM activity_log

            WHERE event_type = ?

            ORDER BY timestamp DESC

            LIMIT 1
            """,
            (event_type,),
        )

        return cursor.fetchone()

    # ---------------------------------------------------------
    # Clear log
    # ---------------------------------------------------------

    def clear(self):

        self.connection.connection.execute(
            "DELETE FROM activity_log"
        )

        self.connection.commit()