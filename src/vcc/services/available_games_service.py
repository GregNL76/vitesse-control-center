from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse

import requests

from src.vcc.config import DATA_DIR


class NswgfGamesParser(HTMLParser):
    """Extract the title links from NSWGF's all-games list."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_listing_item = False
        self.in_title_link = False
        self.current_url = None
        self.current_title = []
        self.games = []

    @staticmethod
    def _classes(attributes):
        values = dict(attributes).get("class", "")
        return set(values.split())

    def handle_starttag(self, tag, attributes):
        tag = tag.lower()
        if tag == "li" and "listing-item" in self._classes(attributes):
            self.in_listing_item = True
            return

        if (
            tag == "a"
            and self.in_listing_item
            and "title" in self._classes(attributes)
        ):
            self.current_url = dict(attributes).get("href")
            self.current_title = []
            self.in_title_link = True

    def handle_data(self, data):
        if self.in_title_link:
            self.current_title.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "a" and self.in_title_link:
            title = " ".join("".join(self.current_title).split())
            parsed_url = urlparse(self.current_url or "")
            if (
                title
                and parsed_url.scheme in {"http", "https"}
                and parsed_url.netloc.lower() in {"nswgf.com", "www.nswgf.com"}
            ):
                self.games.append({"title": title, "url": self.current_url})
            self.in_title_link = False
            self.current_url = None
            self.current_title = []
        elif tag == "li":
            self.in_listing_item = False


class AvailableGamesService:
    SOURCE_URL = "https://nswgf.com/list-all-game-switch/"
    CACHE_FILE = DATA_DIR / "nswgf_available_games.json"
    CACHE_TTL = timedelta(days=1)
    TIMEOUT = 60

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def _load_cache(self):
        try:
            payload = json.loads(self.CACHE_FILE.read_text("utf-8"))
            if not isinstance(payload.get("games"), list):
                return None
            return payload
        except (OSError, ValueError, AttributeError):
            return None

    @staticmethod
    def _parse_timestamp(value):
        try:
            timestamp = datetime.fromisoformat(str(value))
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            return timestamp.astimezone(timezone.utc)
        except (TypeError, ValueError):
            return None

    def _cache_is_fresh(self, payload: dict) -> bool:
        fetched_at = self._parse_timestamp(payload.get("fetched_at"))
        return bool(
            fetched_at
            and datetime.now(timezone.utc) - fetched_at < self.CACHE_TTL
        )

    def _download(self) -> list[dict]:
        response = self.session.get(
            self.SOURCE_URL,
            headers={"User-Agent": "Vitesse-Control-Center/1.0"},
            timeout=self.TIMEOUT,
        )
        response.raise_for_status()

        parser = NswgfGamesParser()
        parser.feed(response.text)
        parser.close()

        if not parser.games:
            raise ValueError("NSWGF returned no game titles")

        unique = {}
        for game in parser.games:
            unique[game["url"]] = game
        return sorted(unique.values(), key=lambda item: item["title"].casefold())

    def _write_cache(self, payload: dict):
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.CACHE_FILE.with_suffix(".download")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temporary, self.CACHE_FILE)

    def _save_cache(self, games: list[dict]) -> dict:
        payload = {
            "source": self.SOURCE_URL,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "games": games,
        }
        self._write_cache(payload)
        return payload

    def get(self) -> dict:
        cached = self._load_cache()
        if cached is not None and self._cache_is_fresh(cached):
            return dict(cached, stale=False)

        retry_after = self._parse_timestamp(
            cached.get("retry_after") if cached else None
        )
        if retry_after and retry_after > datetime.now(timezone.utc):
            return dict(cached, stale=True)

        try:
            return dict(self._save_cache(self._download()), stale=False)
        except (OSError, ValueError, requests.RequestException):
            if cached is not None:
                cached["retry_after"] = (
                    datetime.now(timezone.utc) + timedelta(hours=1)
                ).isoformat()
                self._write_cache(cached)
                return dict(cached, stale=True)
            raise
