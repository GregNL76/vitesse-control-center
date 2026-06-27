"""
VCC - Library scanner
"""

from __future__ import annotations

import re
from pathlib import Path

from .config import SUPPORTED_EXTENSIONS
from .game import GameFile
from .library import Library


TITLE_RE = re.compile(r"\[([0-9A-Fa-f]{16})\]")
VERSION_RE = re.compile(r"\[v(\d+)\]")


def detect_type(title_id: str) -> str:
    """
    Determine whether this file is a BASE game or UPDATE.

    Update TitleIDs always end with 800.
    """

    if title_id.endswith("800"):
        return "UPDATE"

    return "BASE"


def parse_file(path: Path):

    title_match = TITLE_RE.search(path.name)

    if not title_match:
        return None

    version_match = VERSION_RE.search(path.name)

    version = 0

    if version_match:
        version = int(version_match.group(1))

    title_id = title_match.group(1).upper()

    name = path.name.split("[")[0].strip()

    game_file = GameFile(
        path=path,
        title_id=title_id,
        version=version,
        file_type=detect_type(title_id),
    )

    return name, game_file


def scan(folder) -> Library:

    folder = Path(folder)

    library = Library()

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        result = parse_file(file)

        if result is None:
            continue

        name, game_file = result

        library.add_file(name, game_file)

    return library