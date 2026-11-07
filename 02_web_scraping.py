"""STEP 2 - Web scraping the Falcon 9 launch tables from Wikipedia  (slide 5).
Output: data/spacex_scraped_launches.csv"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from config import DATA

URL = ("https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches"
       "&oldid=1027686922")                      # fixed snapshot of the page used in the course
headers = {"User-Agent": "Mozilla/5.0 (capstone project)"}

html = requests.get(URL, headers=headers, timeout=60).text
soup = BeautifulSoup(html, "html.parser")
print("Page title:", soup.title.string)

tables = soup.find_all("table", class_="wikitable")
print(len(tables), "wikitables found")

frames = []
for t in tables:
    try:
        df = pd.read_html(StringIO(str(t)))[0]
    except ValueError:
        continue
    df.columns = [" ".join(map(str, c)).strip() if isinstance(c, tuple) else str(c) for c in df.columns]
    if any("Launch site" in c for c in df.columns) and any("Booster" in c for c in df.columns):
        frames.append(df)

if not frames:
    raise SystemExit("No launch tables found - Wikipedia's layout may have changed. Print `tables` and inspect.")

launches = pd.concat(frames, ignore_index=True)
launches.to_csv(DATA / "spacex_scraped_launches.csv", index=False)
print(launches.shape)
print(launches.head())
