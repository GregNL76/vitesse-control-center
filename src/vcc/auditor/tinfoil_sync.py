from __future__ import annotations

from datetime import datetime
import requests


class TinfoilSync:
    """
    Download de actuele TitleDB en sla deze op in SQLite.
    """

    TITLEDB_URL = (
        "https://raw.githubusercontent.com/blawar/titledb/master/versions.json"
    )

    def __init__(self, database):
        self.database = database

    def download(self) -> dict:

        print("Downloading TitleDB...")

        response = requests.get(self.TITLEDB_URL, timeout=60)
        response.raise_for_status()

        data = response.json()

        first_key = next(iter(data))

        print("First title:", first_key)
        print("Data:", data[first_key])

        return data

    def normalize(self, data: dict) -> dict:

        synced = datetime.utcnow().isoformat()

        titles = {}

        for title_id, versions in data.items():

            latest_version = max(int(v) for v in versions.keys())

            titles[title_id.upper()] = {
                "title_id": title_id.upper(),
                "name": "Unknown",
                "version": latest_version,
                "synced_at": synced,
            }

        return titles

    def sync(self) -> int:

        raw = self.download()

        titles = self.normalize(raw)

        self.database.save_tinfoil_titles(titles)

        return len(titles)