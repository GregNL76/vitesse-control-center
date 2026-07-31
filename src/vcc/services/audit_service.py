"""
Audit service.
"""

from src.vcc.services.update_service import UpdateService


class AuditService:
    """
    Executes all configured audits.
    """

    def __init__(self, repository, logger):

        self.repository = repository
        self.logger = logger

    def run(self):

        service = UpdateService(self.repository)

        report = service.missing_updates()

        self.logger.info("")
        self.logger.info("Update Auditor")
        self.logger.info("-----------------------------------")
        self.logger.info("Missing updates : %s", len(report))
        self.logger.info("Text report     : reports/missing_updates.txt")
        self.logger.info("CSV report      : reports/missing_updates.csv")
        self.logger.info("HTML report     : reports/missing_updates.html")

        return report