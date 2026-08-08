from src.vcc.database import Database

db = Database()

title_id = "0100544020572800"

print("Game:")
print(db.games.by_title_id(title_id))

print()

print("Tinfoil:")
print(db.tinfoil.get(title_id))

print()

print("Latest:")
print(db.tinfoil.latest_version(title_id))