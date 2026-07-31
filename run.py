"""
Vitesse Control Center

Main entry point.
"""

from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.database import Database
from src.vcc.logger import get_logger
from src.vcc.auditor.tinfoil_sync import TinfoilSync
from src.vcc.auditor.report_writer import ReportWriter
from src.vcc.services.sync_service import SyncService
from src.vcc.tasks import FullRefreshTask

from src.vcc.reporting.console import (
    print_database_stats,
    print_duplicate_updates,
    print_largest_games,
    print_library_summary,
    print_orphan_updates,
    print_repository_stats,
)

def main():

    logger = get_logger()

    logger.info("===================================")
    logger.info("Vitesse Control Center")
    logger.info("===================================")

    database = Database()
    database.initialize()

    try:

        print_database_stats(logger, database)

        FullRefreshTask().run()

    finally:

        database.close()

    logger.info("")
    logger.info("Done.")

if __name__ == "__main__":
    main()