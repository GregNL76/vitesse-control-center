from pathlib import Path


GAMES_FOLDER = Path("/volume1/web/games")


def main():

    print("=" * 60)
    print("Bestanden direct in /games")
    print("=" * 60)
    print()

    files = sorted(
        file
        for file in GAMES_FOLDER.iterdir()
        if file.is_file()
    )

    print(f"Aantal bestanden: {len(files)}")
    print()

    for file in files:
        print(file.name)

    print()
    print("=" * 60)
    print("Klaar")
    print("=" * 60)


if __name__ == "__main__":
    main()