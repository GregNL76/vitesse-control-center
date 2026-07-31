"""
TitleDB synchronization task.
"""

from src.vcc.services.titledb_service import TitleDbService

from .base import BaseTask


class SyncTitleDBTask(BaseTask):
    """
    Executes the TitleDB synchronization task.
    """

    def run(self):

        return TitleDbService(
            self.database,
            self.logger,
        ).run()