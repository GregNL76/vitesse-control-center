"""
Vitesse Control Center

Main entry point.
"""

from src.vcc.config import GAME_FOLDER
from src.vcc.database import Database
from src.vcc.logger import get_logger
from src.vcc.scanner import scan


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


def main():

    logger = get_logger()

    logger.info("===================================")
    logger.info("Vitesse Control Center")
    logger.info("===================================")

    database = Database()
    database.initialize()

    print_database_stats(logger, database)

    logger.info("")
    logger.info("Scanning library...")

    library = scan(GAME_FOLDER)

    database.save_library(library)

    print_library_summary(logger, library)

    print_first_games(logger, library)

    database.close()

    logger.info("")
    logger.info("Done.")


if __name__ == "__main__":
    main()