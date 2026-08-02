from __future__ import annotations

from src.vcc.database import Database
from src.vcc.models.game import Game

class GameService:
    """
    High-level service used by the dashboard, CLI and future REST API.

    This class contains NO SQL.
    All database access goes through Database / DatabaseQueries.
    """

    def __init__(self, database: Database):

        self.database = database

    # -----------------------------------------------------------------

    def all_games(self) -> list[Game]:

        rows = self.database.queries.games_with_latest_versions()

        games = []

        for row in rows:

            games.append(
                Game(
                    title_id=row["title_id"],
                    name=row["name"],
                    publisher=row["publisher"],
                    developer=row["developer"],
                    installed_version=row["installed_version"],
                    latest_version=row["latest_version"],
                    update_available=bool(row["update_available"]),
                    release_date=row["release_date"],
                    rating=row["rating"],
                    icon_url=row["icon_url"],
                    banner_url=row["banner_url"],
                    languages=row["languages"],
                    categories=row["categories"],
                )
            )

        return games

    # -----------------------------------------------------------------

    def games_api(self):

        """
        Return games formatted for the AG Grid frontend.
        """

        rows = []

        for game in self.all_games():

            installed = game.installed_version or 0
            latest = game.latest_version or 0

            if latest == 0:

                status = {
                    "text": "Unknown",
                    "color": "#6c757d"
                }

            elif installed < latest:

                status = {
                    "text": "Update",
                    "color": "#dc3545"
                }

            else:

                status = {
                    "text": "Current",
                    "color": "#198754"
                }

            rows.append({

                "title_id": game.title_id,

                "name": game.name,

                "publisher": game.publisher,

                "developer": game.developer,

                "installed": installed,

                "latest": latest,

                "installed_display": (
                    f"v{installed}"
                    if installed
                    else "-"
                ),

                "latest_display": (
                    f"v{latest}"
                    if latest
                    else "-"
                ),

                "status": status,

                "release_date": game.release_date,

                "rating": game.rating,

                "icon_url": game.icon_url,

                "banner_url": game.banner_url,

                "languages": game.languages,

                "categories": game.categories,

                "external_links": {

                    "game_page":
                        f"https://tinfoil.io/Title/{game.title_id}",

                    "search":
                        f"https://www.google.com/search?q={game.name}"

                }

            })

        return rows
        
    def game(self, title_id: str):

        """
        Return one game.
        """

        return self.database.queries.game(title_id)

    # -----------------------------------------------------------------

    def search(self, text: str):

        """
        Search by game name.
        """

        return self.database.queries.search(text)

    # -----------------------------------------------------------------

    def missing_updates(self):

        """
        Return all games that have an update available.
        """

        return self.database.queries.missing_updates()

    # -----------------------------------------------------------------

    def largest_games(self, limit: int = 10):

        """
        Return the largest installed games.
        """

        return self.database.queries.largest_games(limit)

    # -----------------------------------------------------------------

    def statistics(self):

        stats = self.database.queries.statistics()

        stats["tinfoil_titles"] = self.database.tinfoil.count()

        stats["metadata_titles"] = self.database.metadata_count()

        stats["missing_updates"] = len(
            self.database.queries.missing_updates()
        )

        return stats

    # -----------------------------------------------------------------

    def publishers(self):

        """
        Return all publishers.
        """

        return self.database.queries.publishers()

    # -----------------------------------------------------------------

    def categories(self):

        """
        Return all categories.
        """

        return self.database.queries.categories()

    # -----------------------------------------------------------------

    def languages(self):

        """
        Return all languages.
        """

        return self.database.queries.languages()