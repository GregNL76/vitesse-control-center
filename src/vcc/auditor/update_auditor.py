"""
VCC - Update auditor

Compares installed game versions with the latest versions
available in the locally synchronized Tinfoil database.
"""

from __future__ import annotations
from src.vcc.url_builder import UrlBuilder
from src.vcc.sources.nx_versions import NxVersionsSource

class UpdateAuditor:

    def __init__(self, repository, nx_versions=None):

        self.repository = repository
        self.nx_versions = nx_versions or NxVersionsSource()

    # -------------------------------------------------------------

    def audit(self):

        """
        Returns games with an update in Tinfoil or cached nx-versions.
        """

        report = []

        games = self.repository.games_with_latest_versions()

        for game in games:

            installed = game["installed_version"]
            tinfoil_latest = game["latest_version"]
            update_title_id = game["title_id"][:13] + "800"
            nx_latest = self.nx_versions.latest_version(update_title_id) or 0
            latest = max(tinfoil_latest, nx_latest)

            if latest > installed:

                report.append(
                    {
                        "title_id": game["title_id"],
                        "name": game["name"],
                        "installed": installed,
                        "latest": latest,
                        "tinfoil_latest": tinfoil_latest,
                        "nx_versions_latest": nx_latest,
                        "sources_disagree": (
                            tinfoil_latest > 0
                            and nx_latest > 0
                            and tinfoil_latest != nx_latest
                        ),

                        "url": UrlBuilder.tinfoil_url(game["title_id"]),

                        "search_url":
                            UrlBuilder.search_url(game["name"]),

                        "search2_url":
                            UrlBuilder.search2_url(game["name"]),

                        "search3_url":
                            UrlBuilder.search3_url(game["name"]),

                        "search4_url":
                            UrlBuilder.search4_url(game["name"]),
 
 			"search5_url":
                            UrlBuilder.search5_url(game["name"]),
 			}
                )

        return sorted(
            report,
            key=lambda row: row["name"].lower(),
        )
