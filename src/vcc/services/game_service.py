from src.vcc.repository import Repository


class GameService:

    def __init__(self, repository: Repository):

        self.repository = repository

    @staticmethod
    def format_version(version: int) -> str:

        if version <= 0:
            return "-"

        return f"{version} (v{version // 65536})"

    @staticmethod
    def build_status(installed: int, latest: int):

        if latest == 0:
            return {
                "text": "Unknown",
                "color": "#6b7280"
            }

        if installed >= latest:
            return {
                "text": "Current",
                "color": "#16a34a"
            }

        return {
            "text": "Update",
            "color": "#ea580c"
        }

    def games(self):

        rows = self.repository.games_with_latest_versions()

        result = []

        for row in rows:

            installed = row["installed_version"]
            latest = row["latest_version"]

            result.append({

                "title_id": row["title_id"],
                "name": row["name"],

                "installed": installed,
                "installed_display": self.format_version(installed),

                "latest": latest,
                "latest_display": self.format_version(latest),

                "status": self.build_status(installed, latest)

            })

        return result