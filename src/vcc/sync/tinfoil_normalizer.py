from __future__ import annotations

from datetime import datetime


class TinfoilNormalizer:

    def normalize(self, raw: dict) -> dict:

        synced = datetime.utcnow().isoformat()

        titles = {}

        for title_id, versions in raw.items():

            latest = max(
                int(v)
                for v in versions.keys()
            )

            titles[title_id.upper()] = {

                "title_id": title_id.upper(),

                "version": latest,

                "synced_at": synced,

            }

        return titles