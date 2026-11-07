"""STEP 7 - Plotly Dash dashboard  (slides 9, 15).
Run:  python 07_dash_app.py   then open http://127.0.0.1:8050 and take screenshots.
Press Ctrl+C in the terminal to stop it."""
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from config import load_clean

_d = load_clean()
df = _d[["LaunchSite", "PayloadMass", "Class", "BoosterVersion"]].rename(
       columns={"LaunchSite": "Launch Site", "PayloadMass": "Payload Mass (kg)",
                "Class": "class", "BoosterVersion": "Booster Version Category"})
min_p, max_p = df["Payload Mass (kg)"].min(), df["Payload Mass (kg)"].max()

app = Dash(__name__)
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(id="site-dropdown",
                 options=[{"label": "All Sites", "value": "ALL"}] +
                         [{"label": s, "value": s} for s in df["Launch Site"].unique()],
                 value="ALL", placeholder="Select a launch site", searchable=True),
    dcc.Graph(id="success-pie-chart"),
    html.P("Payload range (kg):"),
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000, value=[min_p, max_p],
                    marks={i: str(i) for i in range(0, 10001, 2500)}),
    dcc.Graph(id="success-payload-scatter-chart"),
])


@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def update_pie(site):
    if site == "ALL":
        return px.pie(df, values="class", names="Launch Site", title="Total successful launches by site")
    d = df[df["Launch Site"] == site]["class"].value_counts().reset_index()
    d.columns = ["class", "count"]
    return px.pie(d, values="count", names="class", title=f"Success (1) vs failure (0) for {site}")


@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def update_scatter(site, payload):
    d = df[df["Payload Mass (kg)"].between(payload[0], payload[1])]
    if site != "ALL":
        d = d[d["Launch Site"] == site]
    return px.scatter(d, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                      title="Payload vs launch outcome")


if __name__ == "__main__":
    app.run(debug=False)
