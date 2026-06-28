from src.vcc.auditor.tinfoil_sync import TinfoilSync
from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.auditor.report_writer import ReportWriter
from src.vcc.repository import Repository


class UpdateService:

    def __init__(self, database):

        self.database = database

        self.repository = Repository(database)

    def run(self):

        auditor = UpdateAuditor(self.repository)

        report = auditor.audit()

        ReportWriter().write(report)

        return report