import tempfile
import unittest
from pathlib import Path

from src.vcc.database import Database
from src.vcc.game import GameFile
from src.vcc.library import Library


class ScanHistoryTests(unittest.TestCase):
    def test_rename_preserves_original_addition_date(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            database = Database(directory / "test.sqlite")
            database.initialize()

            original_created = "2026-01-02T03:04:05"
            database.connection.execute(
                """
                INSERT INTO games
                (
                    title_id, name, version, file_type, filename,
                    full_path, size, created, modified
                )
                VALUES (?, ?, 0, 'BASE', ?, ?, 1, ?, ?)
                """,
                (
                    "0100ED9018F3E000",
                    "Old name US",
                    "old name US.nsp",
                    "/games/old name US.nsp",
                    original_created,
                    original_created,
                ),
            )
            database.connection.commit()

            renamed_path = directory / "Eiyuden Chronicle.nsp"
            renamed_path.write_bytes(b"test")
            game_file = GameFile(
                path=renamed_path,
                title_id="0100ED9018F3E000",
                version=0,
                file_type="BASE",
            )
            library = Library()
            library.add_file("Eiyuden Chronicle", game_file)

            database.save_library(library)
            row = database.connection.execute(
                "SELECT name, filename, created FROM games"
            ).fetchone()

            self.assertEqual(row["name"], "Eiyuden Chronicle")
            self.assertEqual(row["filename"], "Eiyuden Chronicle.nsp")
            self.assertEqual(row["created"], original_created)
            database.close()


if __name__ == "__main__":
    unittest.main()
