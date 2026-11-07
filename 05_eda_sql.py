"""STEP 5 - EDA with SQL  (slides 8, 13).
Prints each query result, saves them all to outputs/sql_results.txt and as table images."""
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from config import load_clean, OUT

df = load_clean()
tbl = pd.DataFrame({
    "Date": df["Date"], "Booster_Version": df["BoosterVersion"], "Launch_Site": df["LaunchSite"],
    "Payload_Mass__kg_": df["PayloadMass"], "Orbit": df["Orbit"], "Landing_Outcome": df["Outcome"]})
con = sqlite3.connect(":memory:")
tbl.to_sql("SPACEXTBL", con, index=False)

QUERIES = {
    "1 Unique launch sites": "SELECT DISTINCT Launch_Site FROM SPACEXTBL",
    "2 Sites beginning with CCA": "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5",
    "3 Average payload, booster F9 v1.1": "SELECT AVG(Payload_Mass__kg_) AS avg_payload_kg FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'",
    "4 Date of first successful landing": "SELECT MIN(Date) AS first_successful_landing FROM SPACEXTBL WHERE Landing_Outcome LIKE 'True%'",
    "5 Drone-ship successes, payload 4000-6000 kg": "SELECT DISTINCT Booster_Version, Payload_Mass__kg_ FROM SPACEXTBL WHERE Landing_Outcome = 'True ASDS' AND Payload_Mass__kg_ BETWEEN 4000 AND 6000",
    "6 Landing outcome counts": "SELECT Landing_Outcome, COUNT(*) AS total FROM SPACEXTBL GROUP BY Landing_Outcome ORDER BY total DESC",
    "7 Heaviest payloads": "SELECT Booster_Version, Payload_Mass__kg_ FROM SPACEXTBL ORDER BY Payload_Mass__kg_ DESC LIMIT 5",
    "8 Launches per site": "SELECT Launch_Site, COUNT(*) AS launches FROM SPACEXTBL GROUP BY Launch_Site ORDER BY launches DESC",
    "9 Outcome ranking 2010-06-04 to 2017-03-20": "SELECT Landing_Outcome, COUNT(*) AS total FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY total DESC",
}

lines = []
for name, sql in QUERIES.items():
    res = pd.read_sql(sql, con)
    print(f"\n--- {name}\n{sql}\n{res.to_string(index=False)}")
    lines.append(f"--- {name}\n{sql}\n{res.to_string(index=False)}\n")
    fig, ax = plt.subplots(figsize=(8, 0.5 + 0.35 * (len(res) + 1)))
    ax.axis("off")
    if res.empty:
        ax.text(0.5, 0.5, "No rows returned", ha="center")
    else:
        t = ax.table(cellText=res.round(2).values, colLabels=res.columns, loc="center")
        t.auto_set_font_size(False); t.set_fontsize(10); t.scale(1, 1.3)
    ax.set_title(name, fontsize=11)
    fig.savefig(OUT / f"sql_{name.split()[0]}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

(OUT / "sql_results.txt").write_text("\n".join(lines))
print("\nSaved results to", OUT)
