"""
Library scan task.
"""

from src.vcc.workflows import ScanLibraryWorkflow

from .base import BaseTask


class ScanLibraryTask(BaseTask):
    """
    Executes the library scan task.
    """

    def run(self):

        return ScanLibraryWorkflow(
            self.database,
            self.repository,
            self.logger,
        ).run()