from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

from src.vcc.sync.tinfoil_downloader import TinfoilDownloader
from src.vcc.sync.tinfoil_normalizer import TinfoilNormalizer

print("Downloading...")

raw = TinfoilDownloader().download()

print(f"Downloaded: {len(raw)} titles")

titles = TinfoilNormalizer().normalize(raw)

print(f"Normalized: {len(titles)} titles")

first = next(iter(titles))

print("First TitleID :", first)
print("First Record  :", titles[first])