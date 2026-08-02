from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.vcc.database import Database
from src.vcc.sync.tinfoil_sync import TinfoilSync

db = Database()

db.initialize()

result = TinfoilSync(db).sync()

print(result)

print("Rows:", db.tinfoil.count())