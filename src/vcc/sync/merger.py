from __future__ import annotations


class TitleDBMerger:
    """
    Merge Dutch and English TitleDB metadata.

    The JSON files are keyed by NSUID.

    VCC uses TitleID as primary key.

    Dutch metadata has priority over English.
    """

    @staticmethod
    def merge(
        dutch: dict,
        english: dict,
    ) -> dict[str, dict]:

        merged: dict[str, dict] = {}

        #
        # First load all English titles.
        #

        for record in english.values():

            title_id = record.get("id")

            if not title_id:
                continue

            merged[title_id.upper()] = record

        #
        # Dutch overrides English.
        #

        for record in dutch.values():

            title_id = record.get("id")

            if not title_id:
                continue

            merged[title_id.upper()] = record

        return merged