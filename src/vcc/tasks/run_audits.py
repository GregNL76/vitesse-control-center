"""
Audit task.
"""

from src.vcc.workflows import RunAuditsWorkflow

from .base import BaseTask


class RunAuditsTask(BaseTask):
    """
    Executes all configured auditors.
    """

    def run(self):

        return RunAuditsWorkflow(
            self.repository,
            self.logger,
        ).run()