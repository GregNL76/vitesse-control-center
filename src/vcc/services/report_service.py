from __future__ import annotations

import re
from pathlib import Path

from src.vcc.config import GAME_FOLDER


TITLE_ID_RE = re.compile(r"\[([0-9A-Fa-f]{16})\]")

SUPPORTED_EXTENSIONS = {
    ".nsp",
    ".nsz",
    ".xci",
    ".xcz",
}


class ReportService:

    def invalid_update_title_ids(self) -> list[dict]:

        updates_folder = Path(GAME_FOLDER) / "UPDATES"
        base_folder = Path(GAME_FOLDER) / "BASE"

        problems = []

        # ---------------------------------------------------------
        # Build BASE Title ID lookup
        # ---------------------------------------------------------

        base_files = {}

        if base_folder.exists():

            for file in base_folder.iterdir():

                if not file.is_file():
                    continue

                if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

                match = TITLE_ID_RE.search(file.name)

                if not match:
                    continue

                title_id = match.group(1).upper()

                base_files[title_id] = file.name

        # ---------------------------------------------------------
        # Check UPDATES
        # ---------------------------------------------------------

        if not updates_folder.exists():
            return problems

        for file in sorted(
            updates_folder.iterdir(),
            key=lambda item: item.name.lower(),
        ):

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            match = TITLE_ID_RE.search(file.name)

            size = self._format_size(file.stat().st_size)

            if not match:

                problems.append({
                    "filename": file.name,
                    "size": size,
                    "title_id": None,
                    "base_id": None,
                    "base_filename": None,
                    "expected_id": None,
                    "problem": "No valid Title ID",
                })

                continue

            title_id = match.group(1).upper()

            if not title_id.endswith("800"):

                base_filename = base_files.get(title_id)

                expected_id = (
                    title_id[:-3] + "800"
                    if title_id.endswith("000")
                    else None
                )

                if base_filename:
                    problem = "BASE Title ID used for update"
                else:
                    problem = "Title ID does not end in 800"

                problems.append({
                    "filename": file.name,
                    "size": size,
                    "title_id": title_id,
                    "base_id": title_id if base_filename else None,
                    "base_filename": base_filename,
                    "expected_id": expected_id,
                    "problem": problem,
                })

        return problems


    def update_versions_without_v(self) -> list[dict]:

        updates_folder = Path(GAME_FOLDER) / "UPDATES"

        problems = []

        if not updates_folder.exists():
            return problems

        for file in sorted(
            updates_folder.iterdir(),
            key=lambda item: item.name.lower(),
        ):

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            blocks = re.findall(
                r"\[([^\[\]]+)\]",
                file.stem,
            )

            if not blocks:
                continue

            last_block = blocks[-1].strip()

            title_match = TITLE_ID_RE.search(file.name)

            title_id = (
                title_match.group(1).upper()
                if title_match
                else None
            )

            # Als het laatste blok het Title ID zelf is,
            # ontbreekt er een apart versieblok.
            # Dat hoort bij het derde report.
            if (
                title_id
                and last_block.upper() == title_id
            ):
                continue

            # Bijvoorbeeld [65536] in plaats van [v65536]
            if last_block.isdigit():

                problems.append({
                    "filename": file.name,
                    "size": self._format_size(
                        file.stat().st_size
                    ),
                    "version": last_block,
                    "expected": f"v{last_block}",
                    "problem": "Version number missing 'v' prefix",
                })

        return problems


    def invalid_update_version_blocks(self) -> list[dict]:

        updates_folder = Path(GAME_FOLDER) / "UPDATES"

        problems = []

        if not updates_folder.exists():
            return problems

        for file in sorted(
            updates_folder.iterdir(),
            key=lambda item: item.name.lower(),
        ):

            if not file.is_file():
                continue

            if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            blocks = re.findall(
                r"\[([^\[\]]+)\]",
                file.stem,
            )

            title_match = TITLE_ID_RE.search(file.name)

            title_id = (
                title_match.group(1).upper()
                if title_match
                else None
            )

            size = self._format_size(
                file.stat().st_size
            )

            if not blocks:

                problems.append({
                    "filename": file.name,
                    "size": size,
                    "version_block": None,
                    "problem": "No version block found",
                })

                continue

            last_block = blocks[-1].strip()

            # Goed formaat: [v65536]
            if re.fullmatch(
                r"v\d+",
                last_block,
                flags=re.IGNORECASE,
            ):
                continue

            # Alleen nummer: hoort bij Report 2
            if (
                last_block.isdigit()
                and not (
                    title_id
                    and last_block.upper() == title_id
                )
            ):
                continue

            # Het laatste blok is nog het Title ID:
            # dus er staat geen versieblok achter.
            if (
                title_id
                and last_block.upper() == title_id
            ):

                problems.append({
                    "filename": file.name,
                    "size": size,
                    "version_block": None,
                    "problem": "No version block after Title ID",
                })

                continue

            # Alles anders is ongeldig:
            # [Update], [vABC], [version65536], enz.
            problems.append({
                "filename": file.name,
                "size": size,
                "version_block": last_block,
                "problem": "Invalid version block",
            })

        return problems
        
    @staticmethod
    def _format_size(size_bytes: int) -> str:

        size = float(size_bytes)

        for unit in ("B", "KB", "MB", "GB", "TB"):

            if size < 1024 or unit == "TB":
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size_bytes} B"