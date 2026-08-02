from __future__ import annotations

from ..game import GameFile
from ..library import Library


class GameStorage:
    """
    Store scanned game files.
    """

    def __init__(self, connection):

        self.connection = connection

    def clear(self):

        self.connection.connection.execute(
            "DELETE FROM games"
        )

    def insert(
        self,
        name: str,
        game_file: GameFile,
    ):

        self.connection.connection.execute(
            """
            INSERT OR REPLACE INTO games
            (
                title_id,
                name,
                version,
                file_type,
                filename,
                full_path,
                size,
                created,
                modified
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?
            )
            """,
            (
                game_file.title_id,
                name,
                game_file.version,
                game_file.file_type,
                game_file.filename,
                str(game_file.path),
                game_file.size,
                game_file.created.isoformat()
                    if game_file.created else None,
                game_file.modified.isoformat()
                    if game_file.modified else None,
            ),
        )

    def save_library(
        self,
        library: Library,
    ):

        self.clear()

        for game in library.all_games():

            if game.base:

                self.insert(
                    game.name,
                    game.base,
                )

            for update in game.updates:

                self.insert(
                    game.name,
                    update,
                )

        self.connection.commit()