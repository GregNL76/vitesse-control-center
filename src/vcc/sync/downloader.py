from __future__ import annotations

import time

import requests


class TitleDBDownloadError(RuntimeError):
    """Raised when downloading TitleDB data fails."""


class TitleDBDownloader:
    """
    Downloads TitleDB JSON files from the official repository.

    Features

    - automatic retries
    - timeout
    - custom User-Agent
    - consistent error handling
    """

    BASE_URL = (
        "https://raw.githubusercontent.com/blawar/titledb/master"
    )

    USER_AGENT = "Vitesse-Control-Center/1.0"

    TIMEOUT = 30

    RETRIES = 3

    RETRY_DELAY = 2

    def download(self, filename: str) -> dict:

        url = f"{self.BASE_URL}/{filename}"

        headers = {
            "User-Agent": self.USER_AGENT,
        }

        last_exception = None

        for attempt in range(1, self.RETRIES + 1):

            try:

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.TIMEOUT,
                )

                response.raise_for_status()

                return response.json()

            except requests.RequestException as exc:

                last_exception = exc

                if attempt < self.RETRIES:
                    time.sleep(self.RETRY_DELAY)

        raise TitleDBDownloadError(
            f"Unable to download '{filename}' "
            f"after {self.RETRIES} attempts."
        ) from last_exception

    def versions(self) -> dict:

        return self.download("versions.json")

    def dutch(self) -> dict:

        return self.download("NL.nl.json")

    def english(self) -> dict:

        return self.download("US.en.json")