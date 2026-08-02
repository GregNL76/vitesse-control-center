from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.vcc.database import Database
from src.vcc.services.dashboard_service import DashboardService

db = Database()
db.initialize()

dashboard = DashboardService(db)

data = dashboard.overview()

print(data.keys())
print()

print("Statistics")
print(data["statistics"])
print()

print("Largest games :", len(data["largest_games"]))
print("Missing updates:", len(data["missing_updates"]))