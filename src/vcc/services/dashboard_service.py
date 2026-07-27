from src.vcc.repository import Repository


class DashboardService:

    def __init__(self, repository: Repository):

        self.repository = repository

    def statistics(self):

        return self.repository.statistics()
