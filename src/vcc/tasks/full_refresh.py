"""
Full refresh task.
"""

from .base import BaseTask
from .run_audits import RunAuditsTask
from .scan_library import ScanLibraryTask
from .sync_titledb import SyncTitleDBTask


class FullRefreshTask(BaseTask):

    def run(self):

        ScanLibraryTask().run()

        SyncTitleDBTask().run()

        RunAuditsTask().run()