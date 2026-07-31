from src.vcc.url_builder import UrlBuilder


class DuplicateUpdateMapper:

    @staticmethod
    def format_version(version: int) -> str:

        if version <= 0:
            return "-"

        return f"{version} (v{version // 65536})"

    def map(self, rows):

        result = []

        for row in rows:

            result.append(
                {
                    "title_id": row["title_id"],
                    "name": row["name"],
                    "version": row["version"],
                    "version_display": self.format_version(row["version"]),
                    "file_name": row["file_name"],
                    "size": row["size"],
                    "external_links": {
                        "game_page": UrlBuilder.game_page_url(row["name"]),
                        "search": UrlBuilder.game_search_url(row["name"]),
                    },
                }
            )

        return result