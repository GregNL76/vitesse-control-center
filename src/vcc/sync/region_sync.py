from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from json import JSONDecodeError
from pathlib import Path

import requests

from src.vcc.config import DATA_DIR
from src.vcc.regions import base_title_id, classify_region


class StreamingJsonObject:
    """Iterate over a large top-level JSON object without loading it all."""

    def __init__(self, path: Path, chunk_size: int = 1024 * 1024):
        self.path = Path(path)
        self.chunk_size = chunk_size

    def items(self):
        decoder = json.JSONDecoder()

        with self.path.open("r", encoding="utf-8-sig") as handle:
            buffer = ""
            position = 0
            eof = False

            def refill():
                nonlocal buffer, position, eof
                chunk = handle.read(self.chunk_size)
                buffer = buffer[position:] + chunk
                position = 0
                eof = chunk == ""

            def skip_whitespace():
                nonlocal position
                while True:
                    while position < len(buffer) and buffer[position].isspace():
                        position += 1
                    if position < len(buffer) or eof:
                        return
                    refill()

            def next_character():
                skip_whitespace()
                if position >= len(buffer):
                    raise ValueError("Unexpected end of TitleDB JSON")
                return buffer[position]

            def decode_value():
                nonlocal position
                while True:
                    skip_whitespace()
                    try:
                        value, end = decoder.raw_decode(buffer, position)
                        position = end
                        return value
                    except JSONDecodeError:
                        if eof:
                            raise
                        refill()

            refill()
            if next_character() != "{":
                raise ValueError("TitleDB JSON must contain a top-level object")
            position += 1

            while True:
                character = next_character()
                if character == "}":
                    return

                key = decode_value()
                if not isinstance(key, str):
                    raise ValueError("TitleDB JSON contains a non-string key")

                if next_character() != ":":
                    raise ValueError("Invalid TitleDB JSON object")
                position += 1

                yield key, decode_value()

                character = next_character()
                if character == "}":
                    return
                if character != ",":
                    raise ValueError("Invalid TitleDB JSON separator")
                position += 1


class TitleRegionSync:
    URL = "https://tinfoil.media/repo/db/titles.json"
    CACHE_FILE = DATA_DIR / "tinfoil_titles.json"
    CACHE_METADATA_FILE = DATA_DIR / "tinfoil_titles.cache.json"
    CACHE_TTL = timedelta(days=1)
    TIMEOUT = (15, 180)

    def __init__(self, database, session=None):
        self.database = database
        self.session = session or requests.Session()

    @staticmethod
    def _library_title_ids(database) -> set[str]:
        cursor = database.connection.execute(
            "SELECT DISTINCT UPPER(title_id) FROM games"
        )
        return {row[0] for row in cursor.fetchall() if row[0]}

    def _cache_is_fresh(self) -> bool:
        if not self.CACHE_FILE.is_file():
            return False
        modified = datetime.fromtimestamp(
            self.CACHE_FILE.stat().st_mtime,
            tz=timezone.utc,
        )
        return datetime.now(timezone.utc) - modified < self.CACHE_TTL

    def _load_cache_metadata(self) -> dict:
        try:
            return json.loads(self.CACHE_METADATA_FILE.read_text("utf-8"))
        except (OSError, ValueError):
            return {}

    def _download_if_needed(self) -> bool:
        if self._cache_is_fresh():
            return True

        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        metadata = self._load_cache_metadata()
        headers = {"User-Agent": "Vitesse-Control-Center/1.0"}
        if self.CACHE_FILE.is_file() and metadata.get("etag"):
            headers["If-None-Match"] = metadata["etag"]
        if self.CACHE_FILE.is_file() and metadata.get("last_modified"):
            headers["If-Modified-Since"] = metadata["last_modified"]

        try:
            response = self.session.get(
                self.URL,
                headers=headers,
                stream=True,
                timeout=self.TIMEOUT,
            )
        except requests.RequestException:
            if self.CACHE_FILE.is_file():
                return True
            raise

        if response.status_code == 304 and self.CACHE_FILE.is_file():
            os.utime(self.CACHE_FILE, None)
            return True

        try:
            response.raise_for_status()
        except requests.RequestException:
            if self.CACHE_FILE.is_file():
                return True
            raise
        temporary = self.CACHE_FILE.with_suffix(".download")

        try:
            with temporary.open("wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)
            os.replace(temporary, self.CACHE_FILE)
        finally:
            if temporary.exists():
                temporary.unlink()

        cache_metadata = {
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified"),
        }
        metadata_temporary = self.CACHE_METADATA_FILE.with_suffix(".download")
        metadata_temporary.write_text(
            json.dumps(cache_metadata, indent=2),
            encoding="utf-8",
        )
        os.replace(metadata_temporary, self.CACHE_METADATA_FILE)
        return False

    def _find_records(self, title_ids: set[str]) -> dict[str, dict]:
        wanted = title_ids | {base_title_id(title_id) for title_id in title_ids}
        found = {}

        for key, record in StreamingJsonObject(self.CACHE_FILE).items():
            title_id = str(key).upper()
            if title_id not in wanted or not isinstance(record, dict):
                continue

            countries = record.get("regions") or []
            if not isinstance(countries, list):
                countries = []
            source_region = record.get("region")
            found[title_id] = {
                "region": classify_region(source_region, countries),
                "source_region": source_region,
                "countries": countries,
            }

            if len(found) == len(wanted):
                break

        return found

    def sync(self) -> dict:
        title_ids = self._library_title_ids(self.database)
        if not title_ids:
            return {"titles": 0, "matched": 0, "cached": True}

        cached = self._download_if_needed()
        found = self._find_records(title_ids)
        resolved = {}

        for title_id in title_ids:
            family_title_id = base_title_id(title_id)
            source_title_id = title_id
            item = found.get(title_id)
            if item is None or item.get("region") == "UNKNOWN":
                family_item = found.get(family_title_id)
                if family_item is not None and family_item.get("region") != "UNKNOWN":
                    source_title_id = family_title_id
                    item = family_item
            if item is None:
                resolved[title_id] = {
                    "region": "UNKNOWN",
                    "source_region": None,
                    "countries": [],
                    "source_title_id": source_title_id,
                }
                continue

            resolved[title_id] = dict(item, source_title_id=source_title_id)

        self.database.regions.replace(resolved)
        return {
            "titles": len(resolved),
            "matched": sum(
                item["region"] != "UNKNOWN" for item in resolved.values()
            ),
            "cached": cached,
        }
