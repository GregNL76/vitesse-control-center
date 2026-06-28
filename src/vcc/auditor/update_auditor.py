"""
VCC - Update auditor

Compares installed game versions with the latest versions
available in the locally synchronized Tinfoil database.
"""

from __future__ import annotations
from src.vcc.url_builder import UrlBuilder

class UpdateAuditor:

    def __init__(self, repository):

        self.repository = repository

    # -------------------------------------------------------------

    def audit(self):

        """
        Returns a list of games for which a newer update
        exists in the Tinfoil database.
        """

        report = []

        games = self.repository.games_with_latest_versions()

        for game in games:

            installed = game["installed_version"]
            latest = game["latest_version"]

            if latest > installed:

                report.append(
                    {
                        "title_id": game["title_id"],
                        "name": game["name"],
                        "installed": installed, 
                        "latest": latest,
                        "url": UrlBuilder.game_url(game["name"]),
                        "search_url": UrlBuilder.search_url(game["name"]),
                    }
                )

        return sorted(
            report,
            key=lambda row: row["name"].lower(),
        )