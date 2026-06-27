"""
VCC - Tinfoil synchronizer

Downloads the complete Tinfoil title database.

Currently this class only downloads and parses the data.
Writing to SQLite will be added in the next commit.
"""

from __future__ import annotations

import time
from typing import Dict

import requests


BASE_URL = (
    "https://tinfoil.media/Title/ApiJson/"
    "?rating_content="
    "&language="
    "&category="
    "&region=us"
    "&rating=0"
)


class TinfoilSync:

    def __init__(self):

        self.titles: Dict[str, dict] = {}

    # -------------------------------------------------------------

    def download(
        self,
        page_size: int = 1000,
        delay: float = 1.0,
    ):

        """
        Download the complete Tinfoil database.

        Returns a dictionary:

            {
                "010015100B514800": {
                    "title_id": "...",
                    "name": "...",
                    "version": 327680,
                }
            }
        """

        self.titles.clear()

        start = 0
        total = 1

        while start < total:

            url = (
                BASE_URL
                + f"&start={start}"
                + f"&length={page_size}"
            )

            print(f"Downloading {start}/{total}")

            response = requests.get(
                url,
                timeout=60,
            )

            response.raise_for_status()

            payload = response.json()

            total = payload.get(
                "recordsTotal",
                0,
            )

            data = payload.get(
                "data",
                [],
            )

            for item in data:

                title_id = (
                    item.get("id") or ""
                ).upper()

                if not title_id:
                    continue

                version = item.get(
                    "version",
                    0,
                )

                try:
                    version = int(version)
                except Exception:
                    version = 0

                self.titles[title_id] = {

                    "title_id": title_id,

                    "name": item.get(
                        "name",
                        "",
                    ),

                    "version": version,

                    "raw": item,
                }

            start += page_size

            time.sleep(delay)

        return self.titles

    # -------------------------------------------------------------

    @property
    def total_titles(self):

        return len(self.titles)

    # -------------------------------------------------------------

    def version(
        self,
        title_id: str,
    ):

        record = self.titles.get(
            title_id.upper()
        )

        if record is None:
            return None

        return record["version"]

    # -------------------------------------------------------------

    def name(
        self,
        title_id: str,
    ):

        record = self.titles.get(
            title_id.upper()
        )

        if record is None:
            return None

        return record["name"]

    # -------------------------------------------------------------

    def statistics(self):

        return {

            "titles": self.total_titles,

        }