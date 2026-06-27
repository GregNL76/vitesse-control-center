"""
VCC - Game model

Represents one Nintendo Switch title.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Optional


class GameFile:
    """
    Represents one physical NSP/XCI/NSZ/XCZ file.
    """

    def __init__(
        self,
        path: Path,
        title_id: str,
        version: int,
        file_type: str,
    ):

        self.path = Path(path)

        self.filename = self.path.name

        self.stem = self.path.stem

        self.extension = self.path.suffix.lower()

        self.parent = self.path.parent

        self.title_id = title_id.upper()

        self.version = version

        self.file_type = file_type.upper()

        if self.path.exists():

            stat = self.path.stat()

            self.size = stat.st_size

            self.created = datetime.fromtimestamp(stat.st_ctime)

            self.modified = datetime.fromtimestamp(stat.st_mtime)

        else:

            self.size = 0

            self.created = None

            self.modified = None

    # ----------------------------------------------------------

    @property
    def exists(self) -> bool:

        return self.path.exists()

    # ----------------------------------------------------------

    @property
    def size_mb(self) -> float:

        return self.size / 1024 / 1024

    # ----------------------------------------------------------

    @property
    def size_gb(self) -> float:

        return self.size / 1024 / 1024 / 1024

    # ----------------------------------------------------------

    def __repr__(self):

        return (
            f"<GameFile "
            f"{self.file_type} "
            f"{self.title_id} "
            f"v{self.version}>"
        )


class Game:
    """
    Represents one Nintendo Switch game.

    A game consists of:

    - one Base game
    - zero or more Updates
    - later:
        - DLC
    """

    def __init__(self, name: str):

        self.name = name

        self.base: Optional[GameFile] = None

        self.updates: List[GameFile] = []

        self.latest_available_version = 0

    # ----------------------------------------------------------

    @property
    def has_base(self):

        return self.base is not None

    # ----------------------------------------------------------

    @property
    def has_updates(self):

        return len(self.updates) > 0

    # ----------------------------------------------------------

    @property
    def installed_version(self):

        if not self.updates:
            return 0

        return max(update.version for update in self.updates)

    # ----------------------------------------------------------

    @property
    def base_title_id(self):

        if self.base is None:
            return None

        return self.base.title_id

    # ----------------------------------------------------------

    @property
    def update_title_id(self):

        if self.base is None:
            return None

        return self.base.title_id[:-3] + "800"

    # ----------------------------------------------------------

    @property
    def total_files(self):

        return int(self.has_base) + len(self.updates)

    # ----------------------------------------------------------

    @property
    def total_size(self):

        total = 0

        if self.base:
            total += self.base.size

        total += sum(update.size for update in self.updates)

        return total

    # ----------------------------------------------------------

    @property
    def status(self):

        if not self.has_base:
            return "ORPHAN_UPDATE"

        if (
            self.latest_available_version > self.installed_version
        ):
            return "UPDATE_AVAILABLE"

        return "OK"

    # ----------------------------------------------------------

    def add_file(self, game_file: GameFile):

        if game_file.file_type == "BASE":

            self.base = game_file

            return

        if game_file.file_type == "UPDATE":

            self.updates.append(game_file)

            self.updates.sort(
                key=lambda item: item.version,
                reverse=True
            )

    # ----------------------------------------------------------

    def __repr__(self):

        return (
            f"<Game "
            f"{self.name} "
            f"base={self.has_base} "
            f"updates={len(self.updates)} "
            f"installed={self.installed_version}>"
        )