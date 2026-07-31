"""
Full refresh task.
"""

from .base import BaseTask
from .run_audits import RunAuditsTask
from .scan_library import ScanLibraryTask
from .sync_titledb import SyncTitleDBTask


class FullRefreshTask(BaseTask):
    """
    Executes a complete VCC refresh.
    """

    def run(self):

        ScanLibraryTask(
            self.database,
            self.repository,
        ).run()

        SyncTitleDBTask(
            self.database,
            self.repository,
        ).run()

        RunAuditsTask(
            self.database,
            self.repository,
        ).run()