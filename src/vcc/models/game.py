from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Game:

    title_id: str

    name: str

    publisher: str | None = None
    developer: str | None = None

    installed_version: int = 0
    latest_version: int = 0

    update_available: bool = False

    release_date: int | None = None

    rating: str | None = None

    icon_url: str | None = None
    banner_url: str | None = None

    languages: str | None = None
    categories: str | None = None

    region: str = "UNKNOWN"

    def has_update(self) -> bool:

        return self.latest_version > self.installed_version

    @property
    def version_string(self) -> str:

        return f"{self.installed_version} → {self.latest_version}"

    @property
    def publisher_name(self) -> str:

        return self.publisher or "Unknown"

    @property
    def release_year(self):

        if not self.release_date:
            return None

        return str(self.release_date)[:4]
