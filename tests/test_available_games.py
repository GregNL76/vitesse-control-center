import unittest

from src.vcc.services.available_games_service import NswgfGamesParser


class AvailableGamesParserTests(unittest.TestCase):
    def test_extracts_only_nswgf_listing_titles(self):
        parser = NswgfGamesParser()
        parser.feed(
            """
            <ol class="display-posts-listing">
              <li class="listing-item"><a class="title" href="https://nswgf.com/game-one/">Game &amp; One</a></li>
              <li class="listing-item"><a class="title" href="https://example.com/bad/">Bad host</a></li>
            </ol>
            """
        )
        parser.close()
        self.assertEqual(parser.games, [{
            "title": "Game & One",
            "url": "https://nswgf.com/game-one/",
        }])


if __name__ == "__main__":
    unittest.main()
