"""
Inspect the NX-DB metadata structure.

This tool is for development only.

It downloads the complete NX-DB database and prints useful
information so we can design the VCC Metadata Engine.
"""

from __future__ import annotations

import json
from collections import Counter

import requests

NXDB_URL = (
    "https://raw.githubusercontent.com/ghost-land/NX-DB/refs/heads/main/fulldb.json"
)


def main():

    print("=" * 70)
    print("Downloading NX-DB...")
    print("=" * 70)

    response = requests.get(NXDB_URL, timeout=60)
    response.raise_for_status()

    data = response.json()

    print()
    print(f"Total records : {len(data):,}")

    print(json.dumps(data, indent=4)[:5000])
    return

    print()
    print("=" * 70)
    print("AVAILABLE FIELDS")
    print("=" * 70)

    for key in sorted(first.keys()):
        print(key)

    print()
    print("=" * 70)
    print("FIRST RECORD")
    print("=" * 70)

    print(json.dumps(first, indent=4, ensure_ascii=False))

    with open("sample_nxdb.json", "w", encoding="utf-8") as fp:
        json.dump(first, fp, indent=4, ensure_ascii=False)

    print()
    print("=" * 70)
    print("FIELD ANALYSIS")
    print("=" * 70)

    field_counter = Counter()

    for record in data:
        for key in record.keys():
            field_counter[key] += 1

    for key in sorted(field_counter):
        print(f"{key:30} {field_counter[key]:8}")

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()