from pathlib import Path
import sqlite3
import shutil
from datetime import datetime


DATABASE = Path(
    "/volume1/projects/vitesse-control-center/data/vcc.sqlite"
)

GAMES_FOLDER = Path("/volume1/web/games")

DESTINATIONS = {
    "BASE": GAMES_FOLDER / "BASE",
    "UPDATE": GAMES_FOLDER / "UPDATES",
    "DLC": GAMES_FOLDER / "DLC",
}


def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup = DATABASE.with_name(
        f"{DATABASE.stem}_backup_{timestamp}{DATABASE.suffix}"
    )

    shutil.copy2(DATABASE, backup)

    print(f"Database backup gemaakt:")
    print(f"  {backup}")
    print()


def load_files():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            file_type,
            full_path,
            filename
        FROM games
        ORDER BY file_type, filename
        """
    ).fetchall()

    connection.close()

    return rows


def validate(rows):

    print("Controleren van alle bestanden...")
    print()

    errors = []

    for row in rows:

        file_type = row["file_type"].upper()

        if file_type not in DESTINATIONS:
            errors.append(
                f"Onbekend file_type: "
                f"{file_type} - {row['filename']}"
            )
            continue

        source = Path(row["full_path"])

        if not source.exists():
            errors.append(
                f"Bronbestand bestaat niet: {source}"
            )
            continue

        destination = (
            DESTINATIONS[file_type]
            / row["filename"]
        )

        if destination.exists():
            errors.append(
                f"Doelbestand bestaat al: {destination}"
            )

    if errors:

        print("!!! VALIDATIE MISLUKT !!!")
        print()

        for error in errors:
            print(error)

        print()
        print(
            f"{len(errors)} probleem/problemen gevonden."
        )

        return False

    print(
        f"Alle {len(rows)} bestanden zijn gecontroleerd."
    )

    print("Geen problemen gevonden.")
    print()

    return True


def move_files(rows):

    for destination in DESTINATIONS.values():
        destination.mkdir(
            parents=True,
            exist_ok=True
        )

    counts = {
        "BASE": 0,
        "UPDATE": 0,
        "DLC": 0,
    }

    print("Bestanden verplaatsen...")
    print()

    for index, row in enumerate(rows, start=1):

        file_type = row["file_type"].upper()

        source = Path(row["full_path"])

        destination = (
            DESTINATIONS[file_type]
            / row["filename"]
        )

        shutil.move(
            str(source),
            str(destination)
        )

        counts[file_type] += 1

        print(
            f"[{index}/{len(rows)}] "
            f"{file_type:6} "
            f"{row['filename']}"
        )

    return counts


def main():

    print("=" * 60)
    print("Vitesse Control Center - Game Organizer")
    print("=" * 60)
    print()

    rows = load_files()

    print(f"Bestanden in database : {len(rows)}")
    print()

    # ---------------------------------------------------------
    # 1. Database backup
    # ---------------------------------------------------------

    backup_database()

    # ---------------------------------------------------------
    # 2. Alles controleren
    # ---------------------------------------------------------

    if not validate(rows):

        print()
        print("ER IS NIETS VERPLAATST.")
        return

    # ---------------------------------------------------------
    # 3. Bevestiging
    # ---------------------------------------------------------

    print("=" * 60)
    print("VALIDATIE GESLAAGD")
    print("=" * 60)
    print()
    print("De volgende structuur wordt gebruikt:")
    print()
    print(f"BASE    -> {DESTINATIONS['BASE']}")
    print(f"UPDATES -> {DESTINATIONS['UPDATE']}")
    print(f"DLC     -> {DESTINATIONS['DLC']}")
    print()
    print(f"Totaal bestanden: {len(rows)}")
    print()

    # ---------------------------------------------------------
    # 4. Verplaatsen
    # ---------------------------------------------------------

    counts = move_files(rows)

    # ---------------------------------------------------------
    # 5. Resultaat
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("VERPLAATSING VOLTOOID")
    print("=" * 60)
    print()

    print(f"BASE    : {counts['BASE']}")
    print(f"UPDATES : {counts['UPDATE']}")
    print(f"DLC     : {counts['DLC']}")
    print(
        f"TOTAAL   : "
        f"{sum(counts.values())}"
    )

    print()
    print("Database is NIET aangepast.")
    print(
        "VCC moet nu opnieuw worden gescand "
        "om de nieuwe paden in de database op te nemen."
    )


if __name__ == "__main__":
    main()