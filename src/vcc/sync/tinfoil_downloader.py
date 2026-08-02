from __future__ import annotations

import requests


class TinfoilDownloader:

    URL = (
        "https://raw.githubusercontent.com/blawar/titledb/master/versions.json"
    )

    TIMEOUT = 30

    def download(self) -> dict:

        response = requests.get(
            self.URL,
            timeout=self.TIMEOUT,
        )

        response.raise_for_status()

        return response.json()