"""
Inspect the available metadata in the online Tinfoil TitleDB.

This tool is intended for development only.

It downloads the raw TitleDB metadata and prints the structure of
the first title so we know exactly which fields are available.
"""

from __future__ import annotations

import json
import requests


TITLEDB_URL = (
    "https://raw.githubusercontent.com/blawar/titledb/master/titles.json"
)


def main():

    print("=" * 60)
    print("Downloading TitleDB...")
    print("=" * 60)

    response = requests.get(TITLEDB_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    print()
    print(f"Titles found : {len(data):,}")

    first_key = next(iter(data))
    first_title = data[first_key]

    print()
    print("=" * 60)
    print("First Title ID")
    print("=" * 60)
    print(first_key)

    print()
    print("=" * 60)
    print("Available fields")
    print("=" * 60)

    for key in sorted(first_title.keys()):
        print(key)

    print()
    print("=" * 60)
    print("Complete sample")
    print("=" * 60)

    print(json.dumps(first_title, indent=4, ensure_ascii=False))

    with open("sample_title.json", "w", encoding="utf-8") as fp:
        json.dump(first_title, fp, indent=4, ensure_ascii=False)

    print()
    print("Saved sample_title.json")


if __name__ == "__main__":
    main()