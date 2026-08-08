from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from html.parser import HTMLParser
import re

import requests


class _PatchVersionParser(HTMLParser):
    """Extract patch versions from the Patches table on a Tinfoil.media page."""

    def __init__(self):
        super().__init__()
        self.in_heading = False
        self.heading_parts = []
        self.in_patches = False
        self.in_cell = False
        self.cell_parts = []
        self.versions = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.in_heading = True
            self.heading_parts = []
            return

        if self.in_patches and tag == "td":
            self.in_cell = True
            self.cell_parts = []

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            heading = " ".join(self.heading_parts).strip().lower()
            self.in_heading = False
            self.heading_parts = []

            if heading == "patches":
                self.in_patches = True
            elif self.in_patches:
                self.in_patches = False
            return

        if self.in_patches and tag == "td" and self.in_cell:
            text = " ".join(self.cell_parts).strip()
            match = re.fullmatch(r"v(\d+)", text, flags=re.IGNORECASE)
            if match:
                self.versions.append(int(match.group(1)))

            self.in_cell = False
            self.cell_parts = []

    def handle_data(self, data):
        if self.in_heading:
            self.heading_parts.append(data)
        elif self.in_cell:
            self.cell_parts.append(data)

    def latest_patch_version(self) -> int | None:
        if not self.versions:
            return None
        return max(self.versions) * 65536


class TinfoilSync:
    """
    Synchronize TitleDB versions and supplement them with the latest
    patch version reported by Tinfoil.media.
    """

    TITLEDB_URL = (
        "https://raw.githubusercontent.com/blawar/titledb/master/versions.json"
    )

    TINFOIL_MEDIA_URL = "https://tinfoil.media/Title/{title_id}"

    MEDIA_WORKERS = 6
    MEDIA_TIMEOUT = 20

    def __init__(self, database):
        self.database = database
        self.media_titles_found = 0
        self.media_titles_failed = 0

    def download(self):

        response = requests.get(self.TITLEDB_URL, timeout=30)
        response.raise_for_status()

        return response.json()

    def normalize(self, data: dict) -> dict:

        synced = datetime.utcnow().isoformat()

        titles = {}

        for title_id, versions in data.items():

            if not versions:
                continue

            latest_version = max(int(v) for v in versions.keys())

            titles[title_id.upper()] = {
                "title_id": title_id.upper(),
                "name": "Unknown",
                "version": latest_version,
                "synced_at": synced,
            }

        return titles

    @staticmethod
    def _parse_media_version(html: str) -> int | None:

        parser = _PatchVersionParser()
        parser.feed(html)
        parser.close()

        return parser.latest_patch_version()

    @classmethod
    def _fetch_media_version(cls, title_id: str):

        url = cls.TINFOIL_MEDIA_URL.format(title_id=title_id)

        try:
            response = requests.get(
                url,
                timeout=cls.MEDIA_TIMEOUT,
                headers={
                    "User-Agent": "Vitesse-Control-Center/1.0"
                },
            )
            response.raise_for_status()

            version = cls._parse_media_version(response.text)
            return title_id.upper(), version

        except requests.RequestException:
            return title_id.upper(), None
        except Exception:
            return title_id.upper(), None

    def sync_media_versions(self):

        rows = self.database.queries.all_games()
        title_ids = [row["title_id"].upper() for row in rows]

        versions = {}

        with ThreadPoolExecutor(max_workers=self.MEDIA_WORKERS) as executor:
            futures = {
                executor.submit(self._fetch_media_version, title_id): title_id
                for title_id in title_ids
            }

            for future in as_completed(futures):
                title_id = futures[future]

                try:
                    result_title_id, version = future.result()
                except Exception:
                    result_title_id, version = title_id, None

                if version is None:
                    self.media_titles_failed += 1
                    continue

                versions[result_title_id] = version
                self.media_titles_found += 1

        self.database.tinfoil.save_media_versions(versions)

        return versions

    def sync(self) -> int:

        raw = self.download()

        titles = self.normalize(raw)

        self.database.save_tinfoil_titles(titles)

        self.sync_media_versions()

        return len(titles)
