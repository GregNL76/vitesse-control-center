"""
VCC - Library model

Represents the complete Nintendo Switch library.
"""

from __future__ import annotations

from typing import Dict, List

from .game import Game, GameFile


class Library:
    """
    Complete game library.

    One Game object exists for every Base TitleID.
    """

    def __init__(self):

        # Key = Base TitleID
        self.games: Dict[str, Game] = {}

    # ---------------------------------------------------------

    @staticmethod
    def base_titleid(title_id: str) -> str:
        """
        Convert Update TitleID to Base TitleID.

        Example

        01007E5019ABA800

        becomes

        01007E5019ABA000
        """

        return title_id[:-3] + "000"

    # ---------------------------------------------------------

    def add_file(
        self,
        name: str,
        game_file: GameFile,
    ):

        base_id = self.base_titleid(game_file.title_id)

        if base_id not in self.games:

            self.games[base_id] = Game(name)

        self.games[base_id].add_file(game_file)

    # ---------------------------------------------------------

    @property
    def total_games(self):

        return len(self.games)

    # ---------------------------------------------------------

    @property
    def total_base_games(self):

        return sum(
            1
            for game in self.games.values()
            if game.has_base
        )

    # ---------------------------------------------------------

    @property
    def total_updates(self):

        return sum(
            len(game.updates)
            for game in self.games.values()
        )

    # ---------------------------------------------------------

    @property
    def orphan_updates(self):

        return [
            game
            for game in self.games.values()
            if not game.has_base and game.has_updates
        ]

    # ---------------------------------------------------------

    @property
    def duplicate_updates(self):

        duplicates = []

        for game in self.games.values():

            versions = {}

            for update in game.updates:

                if update.version in versions:

                    duplicates.append(game)
                    break

                versions[update.version] = True

        return duplicates

    # ---------------------------------------------------------

    @property
    def health_score(self):

        score = 100

        score -= len(self.orphan_updates)

        score -= len(self.duplicate_updates)

        if score < 0:
            score = 0

        return score

    # ---------------------------------------------------------

    def all_games(self) -> List[Game]:

        return sorted(
            self.games.values(),
            key=lambda game: game.name.lower()
        )

    # ---------------------------------------------------------

    def summary(self):

        return {
            "games": self.total_games,
            "base_games": self.total_base_games,
            "updates": self.total_updates,
            "orphans": len(self.orphan_updates),
            "duplicate_updates": len(self.duplicate_updates),
            "health": self.health_score,
        }

    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"<Library "
            f"games={self.total_games} "
            f"updates={self.total_updates}>"
        )