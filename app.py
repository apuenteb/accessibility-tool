import dash
from dash import html
import geopandas as gpd
import json

# Load GeoJSON data
sections = gpd.read_file('aggregated_buildings_multipolygons_sections.geojson')
geojson_data = json.loads(sections.to_json())

# Save the Leaflet map HTML with embedded GeoJSON data
with open("leaflet_map.html", "r") as file:
    leaflet_template = file.read()

leaflet_map = leaflet_template.replace("{{ geojson_data }}", json.dumps(geojson_data))

with open("leaflet_map_generated.html", "w") as file:
    file.write(leaflet_map)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Iframe(
            srcDoc=open("leaflet_map_generated.html", "r").read(),
            style={"height": "100vh", "width": "100vw", "border": "none"},
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)

