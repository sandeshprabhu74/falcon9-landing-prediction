"""STEP 6 - Interactive map with Folium  (slides 9, 14).
Creates 3 HTML maps in outputs/. Open them in your browser and screenshot them."""
from math import radians, sin, cos, sqrt, atan2
import folium
from folium.plugins import MarkerCluster, MousePosition
from config import load_clean, OUT

TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
ATTR = "Tiles &copy; Esri"

_df = load_clean()
geo = _df[["LaunchSite", "Latitude", "Longitude", "Class"]].rename(
    columns={"LaunchSite": "Launch Site", "Latitude": "Lat", "Longitude": "Long", "Class": "class"})
sites = geo.groupby("Launch Site")[["Lat", "Long"]].first().reset_index()
print(sites)

# Map 1: launch site markers
m1 = folium.Map(location=[sites.Lat.mean(), sites.Long.mean()], zoom_start=4, tiles=TILES, attr=ATTR)
for _, r in sites.iterrows():
    folium.Circle([r.Lat, r.Long], radius=1000, color="#d35400", fill=True,
                  popup=r["Launch Site"]).add_to(m1)
    folium.Marker([r.Lat, r.Long], icon=folium.DivIcon(
        html=f'<div style="font-size:12px;color:#d35400;white-space:nowrap"><b>{r["Launch Site"]}</b></div>')).add_to(m1)
m1.save(OUT / "map_1_launch_sites.html")

# Map 2: launch records (green = landed, red = failed)
m2 = folium.Map(location=[28.5, -85], zoom_start=4, tiles=TILES, attr=ATTR)
cluster = MarkerCluster().add_to(m2)
for _, r in geo.iterrows():
    folium.Marker([r.Lat, r.Long], popup=r["Launch Site"],
                  icon=folium.Icon(color="green" if r["class"] == 1 else "red")).add_to(cluster)
m2.save(OUT / "map_2_launch_records.html")


# Map 3: proximity analysis for one launch site
def dist_km(a, b):
    R = 6371
    la1, lo1, la2, lo2 = map(radians, [a[0], a[1], b[0], b[1]])
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return 2 * R * atan2(sqrt(h), sqrt(1 - h))


site = sites[sites["Launch Site"].str.contains(r"SLC[- ]40", regex=True)].iloc[0]
site_pt = (site.Lat, site.Long)

# EDIT THESE: open map_3 in your browser, hover over the map (top-right shows coordinates),
# and add the nearest railway and highway points. The two below are approximate examples.
POINTS = {
    "Coastline": (28.56367, -80.57163),
    "City (Titusville)": (28.6122, -80.8076),
    # "Railway": (lat, lon),
    # "Highway": (lat, lon),
}

m3 = folium.Map(location=site_pt, zoom_start=11, tiles=TILES, attr=ATTR)
MousePosition().add_to(m3)
folium.Marker(site_pt, popup=site["Launch Site"], icon=folium.Icon(color="blue")).add_to(m3)
for name, pt in POINTS.items():
    d = dist_km(site_pt, pt)
    print(f"{name}: {d:.2f} km from {site['Launch Site']}")
    folium.Marker(pt, icon=folium.DivIcon(
        html=f'<div style="font-size:12px;white-space:nowrap"><b>{name}: {d:.2f} km</b></div>')).add_to(m3)
    folium.PolyLine([site_pt, pt], weight=2, color="#E8562A").add_to(m3)
m3.save(OUT / "map_3_proximity.html")
print("Maps saved in", OUT)
