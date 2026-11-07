"""STEP 4 - EDA with data visualization  (slides 7, 11, 12).
Charts are saved as PNG files in outputs/."""
import matplotlib.pyplot as plt
import seaborn as sns
from config import load_clean, OUT

sns.set_theme(style="whitegrid")
df = load_clean()


def save_cat(x, y, title, name):
    g = sns.catplot(y=y, x=x, hue="Class", data=df, aspect=2.5)
    g.figure.suptitle(title, y=1.02)
    g.savefig(OUT / name, dpi=150, bbox_inches="tight")
    plt.close("all")


save_cat("FlightNumber", "LaunchSite", "Flight Number vs Launch Site", "eda_01_flight_vs_site.png")
save_cat("PayloadMass", "LaunchSite", "Payload Mass vs Launch Site", "eda_02_payload_vs_site.png")
save_cat("FlightNumber", "Orbit", "Flight Number vs Orbit", "eda_03_flight_vs_orbit.png")
save_cat("PayloadMass", "Orbit", "Payload Mass vs Orbit", "eda_04_payload_vs_orbit.png")

# Bar chart: success rate by orbit
rate = df.groupby("Orbit")["Class"].mean().sort_values(ascending=False)
ax = rate.plot(kind="bar", figsize=(10, 4.5), color="#1F8A8A")
ax.set_ylabel("Success rate"); ax.set_title("Success Rate by Orbit")
plt.tight_layout(); plt.savefig(OUT / "eda_05_success_by_orbit.png", dpi=150); plt.close()

# Line chart: yearly trend
yearly = df.groupby("Year")["Class"].mean()
ax = yearly.plot(marker="o", figsize=(8, 4.5), color="#E8562A")
ax.set_ylabel("Success rate"); ax.set_title("Yearly Launch Success Trend")
plt.tight_layout(); plt.savefig(OUT / "eda_06_yearly_trend.png", dpi=150); plt.close()

print("Success rate by orbit:\n", rate.round(2))
print("\nYearly success rate:\n", yearly.round(2))
print("\nSaved 6 charts to", OUT)
