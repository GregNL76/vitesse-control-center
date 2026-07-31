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

def print_database_stats(logger, database: Database):

    stats = database.stats()

    logger.info("")
    logger.info("Database")
    logger.info("-----------------------------------")
    logger.info("Database file      : %s", stats["database"])
    logger.info("Schema version     : %s", stats["schema"])
    logger.info("Stored game files  : %s", stats["game_files"])


def print_library_summary(logger, library):

    summary = library.summary()

    logger.info("")
    logger.info("Library")
    logger.info("-----------------------------------")
    logger.info("Games              : %s", summary["games"])
    logger.info("Base games         : %s", summary["base_games"])
    logger.info("Updates            : %s", summary["updates"])
    logger.info("Orphan updates     : %s", summary["orphans"])
    logger.info("Duplicate updates  : %s", summary["duplicate_updates"])
    logger.info("Health score       : %s%%", summary["health"])

def print_repository_stats(logger, repo: Repository):

    logger.info("")
    logger.info("Database contents")
    logger.info("-----------------------------------")
    logger.info("Game files         : %s", repo.total_game_files())
    logger.info("Base games         : %s", repo.total_base_games())
    logger.info("Updates            : %s", repo.total_updates())

def print_orphan_updates(logger, repo: Repository):

    orphans = repo.orphan_updates()

    if not orphans:
        return

    logger.info("")
    logger.info("Orphan updates")
    logger.info("-----------------------------------")

    for update in orphans:

        logger.info(
            "%-45s v%-8s %s",
            update["name"],
            update["version"],
            update["title_id"],
        )
         
         
def print_duplicate_updates(logger, repo: Repository):

    duplicates = repo.duplicate_updates()

    if not duplicates:
        return

    logger.info("")
    logger.info("Duplicate updates")
    logger.info("-----------------------------------")

    for update in duplicates:

        logger.info(
            "%-45s v%-8s (%s copies)",
            update["name"],
            update["version"],
            update["duplicates"],
        )


def print_largest_games(logger, repo: Repository):

    logger.info("")
    logger.info("Largest files")
    logger.info("-----------------------------------")

    for row in repo.largest_games():

        logger.info(
            "%-45s %7.2f GB   %s",
            row["name"],
            row["size"] / 1024 / 1024 / 1024,
            row["file_type"],
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