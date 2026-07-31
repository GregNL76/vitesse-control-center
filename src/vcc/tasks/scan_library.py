"""
Library scan task.
"""

from src.vcc.services.scan_service import ScanService

from .base import BaseTask


class ScanLibraryTask(BaseTask):
    """
    Executes the library scan task.
    """

    def run(self):

        return ScanService(
            self.database,
            self.repository,
            self.logger,
        ).run()