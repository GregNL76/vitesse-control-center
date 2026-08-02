from __future__ import annotations


class TinfoilStorage:

    def __init__(self, database):

        self.database = database

    def save(self, titles: dict) -> None:

        self.database.save_tinfoil_titles(
            titles
        )