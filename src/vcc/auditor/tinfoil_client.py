"""
VCC - Tinfoil client
"""

from __future__ import annotations

import requests


API_URL = (
    "https://tinfoil.media/Title/ApiJson/"
    "?rating_content=&language=&category=&region=us&rating=0"
)


class TinfoilClient:

    def __init__(self):

        self._titles = None

    # -------------------------------------------------------------

    def load(self):

        """
        Download complete title database once.
        """

        if self._titles is not None:
            return

        response = requests.get(API_URL, timeout=60)
        response.raise_for_status()

        self._titles = response.json()

    # -------------------------------------------------------------

    def latest_update_version(self, update_title_id: str):

        self.load()

        latest = None

        for title in self._titles:

            if title.get("id", "").upper() != update_title_id.upper():
                continue

            version = int(title.get("version", 0))

            if latest is None or version > latest:
                latest = version

        return latest