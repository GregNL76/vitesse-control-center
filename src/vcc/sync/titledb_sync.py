from __future__ import annotations

import time

from .downloader import TitleDBDownloader
from .merger import TitleDBMerger
from .normalizer import TitleDBNormalizer


class TitleDBSync:
    """
    Synchronizes the official TitleDB.

    Workflow

        versions.json
                │
                ▼

        NL.nl.json
                │
                ▼

        US.en.json
                │
                ▼

        Merge
                │
                ▼

        Normalize
                │
                ▼

        metadata dictionary
    """

    def __init__(self):

        self.downloader = TitleDBDownloader()
        self.merger = TitleDBMerger()
        self.normalizer = TitleDBNormalizer()

    def sync(self) -> dict:

        started = time.perf_counter()

        #
        # Download all required databases
        #

        dutch = self.downloader.dutch()

        english = self.downloader.english()

        #
        # Merge localized metadata
        #

        merged = self.merger.merge(
            dutch=dutch,
            english=english,
        )

        #
        # Normalize into VCC format
        #

        metadata = self.normalizer.normalize(
            titles=merged,
        )

        duration = round(
            time.perf_counter() - started,
            2,
        )

        duration = round(
            time.perf_counter() - started,
            2,
        )

        return {

            "metadata": metadata,

            "statistics": {
                "titles": len(metadata),
                "dutch_titles": len(dutch),
                "english_titles": len(english),
                "duration": duration,
            },
        }