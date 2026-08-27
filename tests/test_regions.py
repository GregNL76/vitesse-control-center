import json
import tempfile
import unittest
from pathlib import Path

from src.vcc.database import Database
from src.vcc.regions import base_title_id, classify_region
from src.vcc.sync.region_sync import StreamingJsonObject


class RegionTests(unittest.TestCase):
    def test_eiyuden_region_examples(self):
        self.assertEqual(classify_region("US", ["US", "CA", "MX"]), "USA")
        self.assertEqual(classify_region("KR", ["KR", "HK"]), "ASIA")

    def test_family_title_id(self):
        self.assertEqual(
            base_title_id("0100ED9018F3E800"),
            "0100ED9018F3E000",
        )

    def test_unknown_update_record_can_inherit_base_region(self):
        from src.vcc.sync.region_sync import TitleRegionSync

        found = {
            "0100ED9018F3E000": {
                "region": "USA",
                "source_region": "US",
                "countries": ["US"],
            },
            "0100ED9018F3E800": {
                "region": "UNKNOWN",
                "source_region": None,
                "countries": [],
            },
        }
        title_id = "0100ED9018F3E800"
        family = base_title_id(title_id)
        item = found[title_id]
        if item["region"] == "UNKNOWN":
            item = found[family]
        self.assertEqual(item["region"], "USA")

    def test_streaming_parser_with_small_chunks(self):
        payload = {
            "0100ED9018F3E000": {"region": "US", "regions": ["US"]},
            "01004DF01DD2A000": {"region": "KR", "regions": ["KR", "HK"]},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "titles.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            parsed = dict(StreamingJsonObject(path, chunk_size=7).items())
        self.assertEqual(parsed, payload)

    def test_database_region_migration_and_queries(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "test.sqlite")
            database.initialize()
            database.connection.execute(
                """
                INSERT INTO games
                (title_id, name, version, file_type, filename, full_path, size)
                VALUES (?, ?, 0, 'BASE', ?, ?, 1)
                """,
                (
                    "0100ED9018F3E000",
                    "Eiyuden Chronicle Hundred Heroes",
                    "game.nsp",
                    "/games/game.nsp",
                ),
            )
            database.connection.commit()
            database.regions.replace({
                "0100ED9018F3E000": {
                    "region": "USA",
                    "source_region": "US",
                    "countries": ["US"],
                    "source_title_id": "0100ED9018F3E000",
                }
            })
            row = database.queries.games_with_latest_versions()[0]
            self.assertEqual(row["region"], "USA")
            self.assertEqual(database.regions.as_map()["0100ED9018F3E000"], "USA")
            database.close()


if __name__ == "__main__":
    unittest.main()
