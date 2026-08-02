from __future__ import annotations


class TitleDBStorage:
    """
    Stores normalized TitleDB metadata in the VCC database.
    """

    def __init__(self, database):

        self.database = database

    def save(self, metadata: dict[str, dict]) -> int:
        """
        Store all normalized metadata.

        Returns
        -------
        int
            Number of stored titles.
        """

        self.database.save_title_metadata(metadata)

        return len(metadata)