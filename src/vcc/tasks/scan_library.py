"""
Library scan task.
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

from .base import BaseTask


class ScanLibraryTask(BaseTask):

    def run(self):

        self.logger.info("")
        self.logger.info("Scanning library...")

        self.logger.info("GAME_FOLDER = %s", GAME_FOLDER)

        library = scan(GAME_FOLDER)

        self.database.save_library(library)

        repo = self.repository

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

        print_library_summary(self.logger, library)
        print_repository_stats(self.logger, repo)
        print_orphan_updates(self.logger, repo)
        print_duplicate_updates(self.logger, repo)
        print_largest_games(self.logger, repo)

        return library