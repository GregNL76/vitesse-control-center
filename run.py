"""
Vitesse Control Center

Main entry point.
"""

from src.vcc.auditor.update_auditor import UpdateAuditor
from src.vcc.config import GAME_FOLDER
from src.vcc.database import Database
from src.vcc.logger import get_logger
from src.vcc.repository import Repository
from src.vcc.scanner import scan
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

        logger.info("")
        logger.info("Scanning library...")

        logger.info("GAME_FOLDER = %s", GAME_FOLDER)
        library = scan(GAME_FOLDER)

        database.save_library(library)

        repo = Repository(database)
        scan_summary = library.summary()
        repo.add_activity(
            event_type="scan",
            severity="success",
            title="Library scan complete",
            message=f"Scanned {scan_summary['games']} game files.",
            details_json={
                "games_scanned": scan_summary["games"],
                "warning_count": 0,
            },
        )

        print_library_summary(logger, library)

        print_repository_stats(logger, repo)

        print_orphan_updates(logger, repo)

        print_duplicate_updates(logger, repo)

        print_largest_games(logger, repo)

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