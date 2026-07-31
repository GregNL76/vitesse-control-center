"""
Library scan workflow.
"""

from src.vcc.config import GAME_FOLDER
from src.vcc.reporting.console import (
    print_duplicate_updates,
    print_largest_games,
    print_library_summary,
    print_orphan_updates,
    print_repository_stats,
)
from src.vcc.scanner import scan


class ScanLibraryWorkflow:
    """
    Executes a complete library scan.
    """

    def __init__(self, database, repository, logger):

        self.database = database
        self.repository = repository
        self.logger = logger

    def run(self):

        self.logger.info("")
        self.logger.info("Scanning library...")

        self.logger.info("GAME_FOLDER = %s", GAME_FOLDER)

        library = scan(GAME_FOLDER)

        self.database.save_library(library)

        summary = library.summary()

        self.repository.add_activity(
            event_type="scan",
            severity="success",
            title="Library scan complete",
            message=f"Scanned {summary['games']} game files.",
            details_json={
                "games_scanned": summary["games"],
                "warning_count": 0,
            },
        )

        print_library_summary(self.logger, library)
        print_repository_stats(self.logger, self.repository)
        print_orphan_updates(self.logger, self.repository)
        print_duplicate_updates(self.logger, self.repository)
        print_largest_games(self.logger, self.repository)

        return library