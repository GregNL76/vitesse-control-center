"""
VCC - Update auditor
"""

from __future__ import annotations

from .tinfoil_client import TinfoilClient


class UpdateAuditor:

    def __init__(self, repository):

        self.repository = repository

        self.client = TinfoilClient()

    # -------------------------------------------------------------

    @staticmethod
    def update_titleid(base_titleid: str):

        return base_titleid[:-3] + "800"

    # -------------------------------------------------------------

    def audit(self):

        report = []

        games = self.repository.all_games()

        for game in games:

            update_titleid = self.update_titleid(game["title_id"])

            latest = self.client.latest_update_version(
                update_titleid
            )

            installed = game["installed_version"]

            if latest is None:
                continue

            if latest > installed:

                report.append(
                    {
                        "name": game["name"],
                        "title_id": game["title_id"],
                        "installed": installed,
                        "latest": latest,
                    }
                )

        return sorted(
            report,
            key=lambda row: row["name"].lower(),
        )