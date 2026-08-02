from __future__ import annotations

from src.vcc.database import Database
from src.vcc.services.game_service import GameService


class DashboardService:
    """
    Provides all data required by the Dashboard.

    The dashboard should only communicate with this service.
    """

    def __init__(self, database: Database):

        self.database = database

        self.games = GameService(database)

    # -----------------------------------------------------------------

    def overview(self) -> dict:

        statistics = self.games.statistics()

        return {

            "statistics": statistics,

            "largest_games": self.games.largest_games(),

            "missing_updates": self.games.missing_updates(),

        }