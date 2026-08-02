from src.vcc.sync.titledb_sync import TitleDBSync
from src.vcc.sync.storage import TitleDBStorage

from src.vcc.sync.tinfoil_sync import TinfoilSync


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

        #
        # ---------------------------------------------------------
        # Tinfoil versions
        # ---------------------------------------------------------
        #

        tinfoil = TinfoilSync(
            self.database
        )

        tinfoil_result = tinfoil.sync()

        #
        # Merge statistics
        #

        result["statistics"]["tinfoil_titles"] = (
            tinfoil_result["titles"]
        )

        result["statistics"]["tinfoil_duration"] = (
            tinfoil_result["duration"]
        )

        return result["statistics"]