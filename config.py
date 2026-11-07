"""Shared settings and helpers. Every script imports this file."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")          # save charts to files instead of opening windows
import pandas as pd
import requests

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

COURSE = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
URLS = {
    "part2": COURSE + "IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/dataset_part_2.csv",
    "geo":   COURSE + "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv",
    "dash":  COURSE + "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv",
}


def get_csv(name):
    """Load data/<name>.csv, downloading it from the course server the first time.
    If the download fails, save the file from your lab page as data/<name>.csv and re-run."""
    local = DATA / f"{name}.csv"
    if not local.exists():
        print(f"Downloading {name} ...")
        try:
            r = requests.get(URLS[name], timeout=60)
            r.raise_for_status()
            local.write_bytes(r.content)
        except Exception as e:
            raise SystemExit(
                f"Could not download {name}: {e}\n"
                f"Download it manually from your course lab and save it as {local}"
            )
    return pd.read_csv(local)


def load_clean():
    """Cleaned dataset produced by 03_data_wrangling.py."""
    path = DATA / "clean.csv"
    if not path.exists():
        raise SystemExit("Run 03_data_wrangling.py first.")
    return pd.read_csv(path)
