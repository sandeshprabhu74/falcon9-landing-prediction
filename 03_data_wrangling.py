"""STEP 3 - Data wrangling  (slide 6).
Outputs: data/clean.csv (labelled data), data/features.csv (one-hot features for modelling)"""
import pandas as pd
from config import get_csv, DATA

df = get_csv("part2")
print("Shape:", df.shape)
print("\nMissing values:\n", df.isnull().sum())
print("\nLaunches per site:\n", df["LaunchSite"].value_counts())
print("\nLaunches per orbit:\n", df["Orbit"].value_counts())
print("\nLanding outcomes:\n", df["Outcome"].value_counts())

# Missing payload mass -> column mean
df["PayloadMass"] = df["PayloadMass"].fillna(df["PayloadMass"].mean())

# Label: 1 = first stage landed, 0 = did not land
bad_outcomes = {"False ASDS", "False Ocean", "False RTLS", "None ASDS", "None None"}
df["Class"] = df["Outcome"].apply(lambda o: 0 if o in bad_outcomes else 1)
df["Year"] = pd.to_datetime(df["Date"]).dt.year
print("\nOverall success rate: %.1f%%" % (df["Class"].mean() * 100))
df.to_csv(DATA / "clean.csv", index=False)

# Features for machine learning
cols = ["FlightNumber", "PayloadMass", "Orbit", "LaunchSite", "Flights", "GridFins", "Reused",
        "Legs", "LandingPad", "Block", "ReusedCount", "Serial"]
features = pd.get_dummies(df[cols], columns=["Orbit", "LaunchSite", "LandingPad", "Serial"]).astype(float)
features.to_csv(DATA / "features.csv", index=False)
print("Feature table:", features.shape)
