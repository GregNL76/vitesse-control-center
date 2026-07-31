"""
Audit task.
"""

from src.vcc.services.audit_service import AuditService

from .base import BaseTask


class RunAuditsTask(BaseTask):
    """
    Executes all configured auditors.
    """

    def run(self):

        return AuditService(
            self.repository,
            self.logger,
        ).run()