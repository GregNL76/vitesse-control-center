"""
Vitesse Control Center

Main entry point.
"""

from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.database import Database
from src.vcc.logger import get_logger
from src.vcc.tasks import ScanLibraryTask
from src.vcc.repository import Repository
from src.vcc.auditor.tinfoil_sync import TinfoilSync
from src.vcc.auditor.report_writer import ReportWriter
from src.vcc.services.update_service import UpdateService
from src.vcc.services.sync_service import SyncService

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

        ScanLibraryTask().run()

        repo = Repository(database)

        count = SyncService(database).run()

        logger.info("")
        logger.info("Tinfoil")
        logger.info("-----------------------------------")
        logger.info("Titles downloaded : %s", count)

        service = UpdateService(repo)

        report = service.missing_updates()
        
        logger.info("")
        logger.info("Update Auditor")
        logger.info("-----------------------------------")
        logger.info("Missing updates : %s", len(report))
        logger.info("Text report     : reports/missing_updates.txt")
        logger.info("CSV report      : reports/missing_updates.csv")  
        logger.info("HTML report     : reports/missing_updates.html")
    
    finally:

        database.close()

    logger.info("")
    logger.info("Done.")


if __name__ == "__main__":
    main()