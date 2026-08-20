"""Cached reader for the nx-versions TitleID/version list."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Optional

import requests

from src.vcc.config import DATA_DIR


class NxVersionsSource:
    """Synchronize and query the nx-versions TitleID -> version list."""

    URL = "https://raw.githubusercontent.com/16BitWonder/nx-versions/master/versions.txt"
    CACHE_FILE = DATA_DIR / "nx_versions.json"
    TIMEOUT = 30

    def __init__(self, cache_file: Optional[Path] = None, session=requests):
        self.cache_file = Path(cache_file or self.CACHE_FILE)
        self.session = session
        self._versions: Optional[Dict[str, int]] = None

    @staticmethod
    def parse(text: str) -> Dict[str, int]:
        """Return valid TitleID/version rows from ``versions.txt``."""
        versions: Dict[str, int] = {}
        for line in text.splitlines():
            title_id, separator, version = line.strip().partition("|")
            if not separator or title_id.lower() == "id":
                continue
            title_id = title_id.upper()
            if len(title_id) != 16 or not all(char in "0123456789ABCDEF" for char in title_id):
                continue
            try:
                versions[title_id] = int(version)
            except ValueError:
                continue
        return versions

    def sync(self) -> dict:
        """Refresh the cache when possible and return sync statistics."""
        cached = self._read_cache()
        headers = {}
        if cached.get("etag"):
            headers["If-None-Match"] = cached["etag"]
        if cached.get("last_modified"):
            headers["If-Modified-Since"] = cached["last_modified"]
        try:
            response = self.session.get(self.URL, headers=headers, timeout=self.TIMEOUT)
            if response.status_code == 304:
                self._versions = cached["versions"]
                return self._result(cached, cached=True)
            response.raise_for_status()
            versions = self.parse(response.text)
            if not versions:
                raise ValueError("nx-versions returned no valid TitleID/version rows")
            payload = {
                "versions": versions,
                "synced_at": datetime.now(timezone.utc).isoformat(),
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
            }
            self._write_cache(payload)
            self._versions = versions
            return self._result(payload, cached=False)
        except (requests.RequestException, ValueError):
            if cached.get("versions"):
                self._versions = cached["versions"]
                return self._result(cached, cached=True)
            raise

    def latest_version(self, title_id: str) -> Optional[int]:
        """Return the cached version for a title, if known."""
        if self._versions is None:
            self._versions = self._read_cache().get("versions", {})
        return self._versions.get(title_id.upper())

    def _read_cache(self) -> dict:
        if not self.cache_file.exists():
            return {}
        try:
            with self.cache_file.open("r", encoding="utf-8") as cache:
                payload = json.load(cache)
        except (OSError, json.JSONDecodeError):
            return {}
        versions = payload.get("versions")
        if not isinstance(versions, dict):
            return {}
        try:
            payload["versions"] = {
                title_id.upper(): int(version)
                for title_id, version in versions.items()
            }
        except (AttributeError, TypeError, ValueError):
            return {}
        return payload

    def _write_cache(self, payload: dict) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", encoding="utf-8", dir=self.cache_file.parent, delete=False) as temporary:
            json.dump(payload, temporary, ensure_ascii=False, sort_keys=True)
            temporary.flush()
            temporary_path = Path(temporary.name)
        temporary_path.replace(self.cache_file)

    @staticmethod
    def _result(payload: dict, cached: bool) -> dict:
        return {
            "titles": len(payload.get("versions", {})),
            "cached": cached,
            "synced_at": payload.get("synced_at"),
        }
