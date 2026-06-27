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


def print_first_games(logger, library):

    logger.info("")
    logger.info("First 10 games")
    logger.info("-----------------------------------")

    for game in library.all_games()[:10]:

        logger.info(
            "%-40s  v%-8s  %s",
            game.name,
            game.installed_version,
            game.status,
        )


def print_repository_stats(logger, repo: Repository):

    logger.info("")
    logger.info("Database contents")
    logger.info("-----------------------------------")
    logger.info("Game files         : %s", repo.total_game_files())
    logger.info("Base games         : %s", repo.total_base_games())
    logger.info("Updates            : %s", repo.total_updates())


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

def run_tinfoil_sync(logger, database):

    logger.info("")
    logger.info("Downloading Tinfoil database")
    logger.info("-----------------------------------")

    sync = TinfoilSync(database)

    count = sync.sync()

    logger.info("")
    logger.info("Tinfoil")
    logger.info("-----------------------------------")
    logger.info("Titles downloaded : %s", count)

   
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

        library = scan(GAME_FOLDER)

        database.save_library(library)

        repo = Repository(database)

        print_library_summary(logger, library)

        print_first_games(logger, library)

        print_repository_stats(logger, repo)

        print_largest_games(logger, repo)

        run_tinfoil_sync(
            logger,
            database,
        )
    
        auditor = UpdateAuditor(repo)

        report = auditor.audit()

        logger.info("")
        logger.info("Update Auditor")
        logger.info("-----------------------------------")
        logger.info("Missing updates : %s", len(report))

        for game in report[:20]:

            logger.info(
                "%-45s installed=%-8s latest=%s",
                game["name"],
                game["installed"],
                game["latest"],
            )   
    
    finally:

        database.close()

    logger.info("")
    logger.info("Done.")


if __name__ == "__main__":
    main()