from src.vcc.auditor.tinfoil_sync import TinfoilSync


class SyncService:

    def __init__(self, database):

        self.database = database

    def run(self):

        sync = TinfoilSync(self.database)

        return sync.sync()