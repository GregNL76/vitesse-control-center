"""
Audit task.
"""

from src.vcc.repository import Repository
from src.vcc.services.update_service import UpdateService

from .base import BaseTask


class RunAuditsTask(BaseTask):

    def run(self):

        repo = Repository(self.database)

        service = UpdateService(repo)

        report = service.missing_updates()

        self.logger.info("")
        self.logger.info("Update Auditor")
        self.logger.info("-----------------------------------")
        self.logger.info("Missing updates : %s", len(report))
        self.logger.info("Text report     : reports/missing_updates.txt")
        self.logger.info("CSV report      : reports/missing_updates.csv")
        self.logger.info("HTML report     : reports/missing_updates.html")

        return report