"""
Console reporting helpers.
"""

from src.vcc.database import Database
from src.vcc.repository import Repository


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