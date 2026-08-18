from pathlib import Path
import shutil


GAMES_FOLDER = Path("/volume1/web/games")

BASE_FOLDER = GAMES_FOLDER / "BASE"
DLC_FOLDER = GAMES_FOLDER / "DLC"


# Deze 10 bestanden zijn BASE-games.
BASE_FILES = {
    "ASTRONEER [0100E63013E60000][v0].nsp",
    "BROK The Brawl Bar [0100AA6025436000][v65536].nsp",
    "BUBBLE BOBBLE SUGAR DUNGEONS [0100471023862000][v0].nsp",
    "Creepy Road [0100C3300C68C000][v0].nsp",
    "Hand in Hand [01002CB01CEE8000][v0].nsp",
    "Hitman Absolution [010037C022390000][v0].nsz",
    "New Super Mario Bros U Deluxe [0100EA80032EA000][v0].nsp",
    "Rayman 30th Anniversary Edition [01007C6025688000][v0].nsp",
    "WRC Generations The Official Game [0100041018810000][v0].xcz",
    "Waifu Uncovered [v0].xcz",
}


def main():

    print("=" * 60)
    print("Vitesse Control Center - Organize Remaining Files")
    print("=" * 60)
    print()

    BASE_FOLDER.mkdir(parents=True, exist_ok=True)
    DLC_FOLDER.mkdir(parents=True, exist_ok=True)

    files = sorted(
        file
        for file in GAMES_FOLDER.iterdir()
        if file.is_file()
    )

    print(f"Bestanden gevonden in /games: {len(files)}")
    print()

    # ---------------------------------------------------------
    # Eerst controleren
    # ---------------------------------------------------------

    errors = []

    for file in files:

        # files.json bewust laten staan
        if file.name == "files.json":
            continue

        if file.name in BASE_FILES:
            destination = BASE_FOLDER / file.name
        else:
            destination = DLC_FOLDER / file.name

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
        print("ER IS NIETS VERPLAATST.")
        return

    # ---------------------------------------------------------
    # Verplaatsen
    # ---------------------------------------------------------

    base_count = 0
    dlc_count = 0

    print("Bestanden verplaatsen...")
    print()

    for file in files:

        # files.json niet aanraken
        if file.name == "files.json":
            continue

        if file.name in BASE_FILES:

            destination = BASE_FOLDER / file.name
            file_type = "BASE"
            base_count += 1

        else:

            destination = DLC_FOLDER / file.name
            file_type = "DLC"
            dlc_count += 1

        print(f"{file_type:4} | {file.name}")

        shutil.move(
            str(file),
            str(destination)
        )

    print()
    print("=" * 60)
    print("VERPLAATSING VOLTOOID")
    print("=" * 60)
    print()

    print(f"BASE : {base_count}")
    print(f"DLC  : {dlc_count}")
    print()
    print("files.json is blijven staan.")
    print()
    print("Totaal verplaatst:",
          base_count + dlc_count)


if __name__ == "__main__":
    main()