"""
URL builder for external game pages.
"""

from __future__ import annotations
from urllib.parse import quote_plus

import re
import unicodedata


class UrlBuilder:

    BASE_URL = "https://nswgame.com"

    @staticmethod
    def slugify(title: str) -> str:
        """
        Convert a game title into an nswgame slug.
        """

        # Unicode -> ASCII
        slug = (
            unicodedata.normalize("NFKD", title)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

        slug = slug.lower()

        replacements = {
            "&": " and ",
            "@": " at ",
            "+": " plus ",
            "'": "",
            '"': "",
            ":": "",
            ";": "",
            ",": "",
            ".": "",
            "!": "",
            "?": "",
            "™": "",
            "®": "",
            "©": "",
            "(": "",
            ")": "",
            "[": "",
            "]": "",
            "{": "",
            "}": "",
            "/": "-",
            "\\": "-",
        }

        for old, new in replacements.items():
            slug = slug.replace(old, new)

        # Alles wat geen letter/cijfer/- is verwijderen
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)

        # Spaties -> -
        slug = re.sub(r"\s+", "-", slug)

        # Dubbele -
        slug = re.sub(r"-+", "-", slug)

        return slug.strip("-")

    
    @classmethod
    def search_url(cls, title: str) -> str:

        return f"{cls.BASE_URL}/?s={quote_plus(title)}"
    
    
    @classmethod
    def game_url(cls, title: str) -> str:

        slug = cls.slugify(title)

        return (
            f"{cls.BASE_URL}/"
            f"{slug}-nintendo-switch-nsp-xci-nsz-download-free/"
        )