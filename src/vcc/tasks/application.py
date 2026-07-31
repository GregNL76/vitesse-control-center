"""
Application task.
"""

from src.vcc.reporting.console import print_database_stats

from .base import BaseTask
from .full_refresh import FullRefreshTask


class ApplicationTask(BaseTask):
    """
    Executes the complete VCC application.
    """

    def run(self):

        print_database_stats(
            self.logger,
            self.database,
        )

        FullRefreshTask(
            self.database,
            self.repository,
        ).run()