from __future__ import annotations

from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.repository import Repository
from src.vcc.url_builder import UrlBuilder


class UpdateService:

    def __init__(self, repository: Repository):
        self.repository = repository

    @staticmethod
    def format_version(version: int) -> str:
        if version <= 0:
            return "-"
        return f"{version} (v{version // 65536})"

    def missing_updates(self):
        return UpdateAuditor(self.repository).audit()

    def orphan_updates(self):

        rows = self.repository.orphan_updates()

        result = []

        for row in rows:

            result.append(
                {
                    "title_id": row["title_id"],
                    "name": row["name"],

                    "version": row["version"],
                    "version_display": self.format_version(row["version"]),

                    "filename": row["filename"],
                    "full_path": row["full_path"],

                    "size": row["size"],

                    "external_links": {
                        "game_page": UrlBuilder.game_page_url(row["name"]),
                        "search": UrlBuilder.game_search_url(row["name"]),
                    },
                }
            )

        return result

    def duplicate_updates(self):

        rows = self.repository.duplicate_update_files()

        result = []

        for row in rows:

            result.append(
                {
                    "title_id": row["title_id"],
                    "name": row["name"],
                    "version": row["version"],
                    "version_display": self.format_version(row["version"]),
                    "file_name": row["file_name"],
                    "size": row["size"],
                    "external_links": {
                        "game_page": UrlBuilder.game_page_url(row["name"]),
                        "search": UrlBuilder.game_search_url(row["name"]),
                    },
                }
            )

        return result