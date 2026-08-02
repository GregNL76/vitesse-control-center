from __future__ import annotations

import time

from .tinfoil_downloader import TinfoilDownloader
from .tinfoil_normalizer import TinfoilNormalizer
from .tinfoil_storage import TinfoilStorage


class TinfoilSync:

    def __init__(self, database):

        self.database = database

        self.downloader = TinfoilDownloader()
        self.normalizer = TinfoilNormalizer()
        self.storage = TinfoilStorage(database)

    def sync(self) -> dict:

        started = time.perf_counter()

        raw = self.downloader.download()

        titles = self.normalizer.normalize(raw)

        self.storage.save(titles)

        duration = round(
            time.perf_counter() - started,
            2,
        )

        return {

            "titles": len(titles),

            "duration": duration,

        }