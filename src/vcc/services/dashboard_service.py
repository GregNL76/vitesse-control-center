from src.vcc.repository import Repository


class DashboardService:

    def __init__(self, repository: Repository):

        self.repository = repository

    def statistics(self):

        stats = self.repository.statistics()

        storage_gb = self.repository.total_storage() / 1024 / 1024 / 1024

        stats.update(
            {
                "dlc": 0,
                "storage": storage_gb,
                "storage_display": f"{storage_gb:.2f} GB",
            }
        )

        return stats

    def library_health(self):

        stats = self.repository.statistics()

        games = self.repository.games_with_latest_versions()

        missing_updates = sum(
            1
            for row in games
            if row["latest_version"] > row["installed_version"]
        )

        health_score = 100 - stats["orphan_updates"] - stats["duplicate_updates"]

        if health_score < 0:
            health_score = 0

        return {
            "health_score": health_score,
            "missing_updates": missing_updates,
            "duplicate_updates": stats["duplicate_updates"],
            "orphan_updates": stats["orphan_updates"],
        }

    def recent_activity(self, limit: int = 5):

        import json
        from datetime import datetime, timedelta

        rows = self.repository.recent_activity(limit)

        activities = []

        for row in rows:

            details = {}

            if row["details_json"]:
                try:
                    details = json.loads(row["details_json"])
                except json.JSONDecodeError:
                    details = {}

            timestamp = datetime.fromisoformat(row["timestamp"])
            now = datetime.utcnow()
            today = now.date()
            yesterday = today - timedelta(days=1)

            if timestamp.date() == today:
                formatted_timestamp = timestamp.strftime("Today %H:%M")
            elif timestamp.date() == yesterday:
                formatted_timestamp = timestamp.strftime("Yesterday %H:%M")
            else:
                formatted_timestamp = timestamp.strftime("%d-%m-%Y %H:%M")

            severity = row["severity"].lower()
            severity_class = {
                "success": "success",
                "warning": "warning",
                "failed": "danger",
            }.get(severity, "secondary")

            activities.append(
                {
                    "id": row["id"],
                    "event_type": row["event_type"],
                    "severity": severity,
                    "severity_class": severity_class,
                    "title": row["title"],
                    "message": row["message"],
                    "formatted_timestamp": formatted_timestamp,
                    "timestamp": row["timestamp"],
                    "details": details,
                    "games_scanned": details.get("games_scanned"),
                    "warning_count": details.get("warning_count"),
                }
            )

        return activities

    def _format_activity_row(self, row):

        import json
        from datetime import datetime, timedelta

        details = {}

        if row["details_json"]:
            try:
                details = json.loads(row["details_json"])
            except json.JSONDecodeError:
                details = {}

        timestamp = datetime.fromisoformat(row["timestamp"])
        now = datetime.utcnow()
        today = now.date()
        yesterday = today - timedelta(days=1)

        if timestamp.date() == today:
            formatted_timestamp = timestamp.strftime("Today %H:%M")
        elif timestamp.date() == yesterday:
            formatted_timestamp = timestamp.strftime("Yesterday %H:%M")
        else:
            formatted_timestamp = timestamp.strftime("%d-%m-%Y %H:%M")

        severity = row["severity"].lower()
        severity_class = {
            "success": "success",
            "warning": "warning",
            "failed": "danger",
        }.get(severity, "secondary")

        return {
            "id": row["id"],
            "event_type": row["event_type"],
            "severity": severity,
            "severity_class": severity_class,
            "title": row["title"],
            "message": row["message"],
            "formatted_timestamp": formatted_timestamp,
            "timestamp": row["timestamp"],
            "details": details,
            "games_scanned": details.get("games_scanned"),
            "warning_count": details.get("warning_count"),
        }

    def last_event(self, event_type: str):

        row = self.repository.last_event(event_type)

        if row is None:
            return None

        return self._format_activity_row(row)
