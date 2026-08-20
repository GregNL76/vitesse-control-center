"""
TitleDB synchronization workflow.
"""

from src.vcc.services.sync_service import SyncService


class SyncTitleDbWorkflow:
    """
    Synchronizes the local TitleDB.
    """

    def __init__(self, database, logger):

        self.database = database
        self.logger = logger

    def run(self):

        count = SyncService(self.database).run()

        self.logger.info("")
        self.logger.info("Data Sources")
        self.logger.info("-----------------------------------")

        self.logger.info("TitleDB")
        self.logger.info("  Titles           : %s", f"{count['titles']:,}")
        self.logger.info("  Dutch titles     : %s", f"{count['dutch_titles']:,}")
        self.logger.info("  English titles   : %s", f"{count['english_titles']:,}")

        self.logger.info("")
        self.logger.info("Tinfoil")
        self.logger.info("  Titles           : %s", f"{count['tinfoil_titles']:,}")
        self.logger.info("  Duration         : %.2f sec", count['tinfoil_duration'])

        self.logger.info("")
        self.logger.info("NX versions")
        self.logger.info("  Titles           : %s", f"{count['nx_versions_titles']:,}")
        self.logger.info(
            "  Cached           : %s",
            "Yes" if count['nx_versions_cached'] else "No"
        )

        self.logger.info("")
        self.logger.info("Total duration     : %.2f sec", count['duration'])

        return count