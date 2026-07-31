"""
TitleDB synchronization task.
"""

from src.vcc.workflows import SyncTitleDbWorkflow

from .base import BaseTask


class SyncTitleDBTask(BaseTask):
    """
    Executes the TitleDB synchronization task.
    """

    def run(self):

        return SyncTitleDbWorkflow(
            self.database,
            self.logger,
        ).run()