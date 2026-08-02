from __future__ import annotations


class TitleDBNormalizer:
    """
    Normalizes merged TitleDB records into the VCC metadata format.
    """

    @staticmethod
    def normalize(
        titles: dict,
    ) -> dict[str, dict]:

        normalized = {}

        for title_id, metadata in titles.items():

            normalized[title_id] = {

                "title_id": title_id,

                "name": metadata.get("name"),

                "publisher": metadata.get("publisher"),

                "developer": metadata.get("developer"),

                "description": metadata.get("description"),

                "intro": metadata.get("intro"),

                "release_date": metadata.get("releaseDate"),

                "categories": metadata.get("category", []),

                "languages": metadata.get("languages", []),

                "players": metadata.get("numberOfPlayers"),

                "rating": metadata.get("rating"),

                "rating_content": metadata.get(
                    "ratingContent",
                    [],
                ),

                "icon_url": metadata.get("iconUrl"),

                "banner_url": metadata.get("bannerUrl"),

                "rights_id": metadata.get("rightsId"),

                "is_demo": metadata.get("isDemo", False),

                "latest_update_id": None,

                "latest_version": None,
            }

        return normalized