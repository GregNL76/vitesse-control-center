"""
URL validator.
"""

from __future__ import annotations

import requests


class UrlValidator:

    @staticmethod
    def exists(url: str) -> bool:

        try:

            response = requests.get(
                url,
                stream=True,
                timeout=2,
            )

            return response.status_code == 200

        except requests.RequestException:

            return False