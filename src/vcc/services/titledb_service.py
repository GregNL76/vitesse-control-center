"""
TitleDB service.
"""

from src.vcc.services.sync_service import SyncService


class TitleDbService:
    """
    Synchronizes the local TitleDB.
    """

    def __init__(self, database, logger):

        self.database = database
        self.logger = logger

    def run(self):

        count = SyncService(self.database).run()

        self.logger.info("")
        self.logger.info("Tinfoil")
        self.logger.info("-----------------------------------")
        self.logger.info("Titles downloaded : %s", count)

        return count