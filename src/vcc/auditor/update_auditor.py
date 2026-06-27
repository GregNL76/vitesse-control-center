"""
VCC - Update auditor

Compares installed game versions with the latest versions
available in the locally synchronized Tinfoil database.
"""

from __future__ import annotations


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

            print(
                game["name"],
                "installed=", installed,
                "latest=", latest,
            )

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