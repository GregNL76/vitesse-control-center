from src.vcc.sync.titledb_sync import TitleDBSync
from src.vcc.sync.storage import TitleDBStorage

import requests

from src.vcc.sync.tinfoil_sync import TinfoilSync
from src.vcc.sync.region_sync import TitleRegionSync
from src.vcc.sources.nx_versions import NxVersionsSource


class SyncService:

    def __init__(self, database):

        self.database = database

    def run(self):

        #
        # ---------------------------------------------------------
        # TitleDB metadata
        # ---------------------------------------------------------
        #

        titledb = TitleDBSync()

        result = titledb.sync()

        TitleDBStorage(
            self.database
        ).save(
            result["metadata"]
        )

        try:
            region_result = TitleRegionSync(self.database).sync()
        except (OSError, ValueError, requests.RequestException):
            region_result = {
                "titles": self.database.regions.count(),
                "matched": self.database.regions.matched_count(),
                "cached": True,
            }

        #
        # ---------------------------------------------------------
        # Tinfoil versions
        # ---------------------------------------------------------
        #

        tinfoil = TinfoilSync(
            self.database
        )

        tinfoil_result = tinfoil.sync()

        # This supplementary source must never stop the existing
        # TitleDB/Tinfoil synchronization when GitHub is unavailable.
        try:
            nx_versions_result = NxVersionsSource().sync()
        except (OSError, ValueError, requests.RequestException):
            nx_versions_result = {"titles": 0, "cached": False}

        #
        # Merge statistics
        #

        result["statistics"]["tinfoil_titles"] = (
            tinfoil_result["titles"]
        )

        result["statistics"]["tinfoil_duration"] = (
            tinfoil_result["duration"]
        )

        result["statistics"]["nx_versions_titles"] = (
            nx_versions_result["titles"]
        )
        result["statistics"]["nx_versions_cached"] = (
            nx_versions_result["cached"]
        )

        result["statistics"]["region_titles"] = region_result["titles"]
        result["statistics"]["region_matched"] = region_result["matched"]
        result["statistics"]["region_cached"] = region_result["cached"]

        return result["statistics"]
