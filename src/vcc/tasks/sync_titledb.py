"""
TitleDB synchronization task.
"""

from src.vcc.services.sync_service import SyncService

from .base import BaseTask


class SyncTitleDBTask(BaseTask):

    def run(self):

        count = SyncService(self.database).run()

        self.logger.info("")
        self.logger.info("Tinfoil")
        self.logger.info("-----------------------------------")
        self.logger.info("Titles downloaded : %s", count)

        return count