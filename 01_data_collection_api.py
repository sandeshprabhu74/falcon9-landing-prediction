"""STEP 1 - Data collection from the SpaceX REST API  (slide 4).
Output: data/spacex_api_launches.csv
Note: the community API can be slow or down. If it fails, skip this step: step 3 uses the
course's prepared dataset, and you can still describe this process on slide 4."""
import time
import pandas as pd
import requests
from config import DATA

API = "https://api.spacexdata.com/v4"
FALCON9_ID = "5e9d0d95eda69973a809d1ec"
cache = {}


def get(endpoint, item_id):
    key = (endpoint, item_id)
    if key not in cache:
        cache[key] = requests.get(f"{API}/{endpoint}/{item_id}", timeout=30).json()
    return cache[key]


launches = requests.get(f"{API}/launches/past", timeout=60).json()
print(f"{len(launches)} past launches downloaded")

rows = []
for i, l in enumerate(launches):
    if l["rocket"] != FALCON9_ID or len(l["cores"]) != 1 or len(l["payloads"]) != 1:
        continue                                     # keep single-core, single-payload Falcon 9 launches
    core, pad = l["cores"][0], get("launchpads", l["launchpad"])
    payload = get("payloads", l["payloads"][0])
    core_info = get("cores", core["core"]) if core["core"] else {}
    landed = core["landing_success"]
    rows.append({
        "FlightNumber": l["flight_number"],
        "Date": l["date_utc"][:10],
        "BoosterVersion": "Falcon 9",
        "PayloadMass": payload.get("mass_kg"),
        "Orbit": payload.get("orbit"),
        "LaunchSite": pad["name"],
        "Outcome": f"{landed} {core['landing_type']}",
        "Flights": core["flight"],
        "GridFins": core["gridfins"],
        "Reused": core["reused"],
        "Legs": core["legs"],
        "LandingPad": core["landpad"],
        "Block": core_info.get("block"),
        "ReusedCount": core_info.get("reuse_count"),
        "Serial": core_info.get("serial"),
        "Longitude": pad["longitude"],
        "Latitude": pad["latitude"],
    })
    if i % 25 == 0:
        print(f"  processed {i} launches"); time.sleep(0.2)

df = pd.DataFrame(rows).sort_values("FlightNumber")
df.to_csv(DATA / "spacex_api_launches.csv", index=False)
print(df.shape); print(df.head())
