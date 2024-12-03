import dash
from dash import dcc, html, Input, Output
from flask import send_file, jsonify
import pandas as pd
import geopandas as gpd
import json

# File paths for demographic data
sociodemographic_files = {
    "mean_age": "path_to_mean_age.csv",
    "average_income": "path_to_average_income.csv",
    "total_population": "path_to_total_population.csv",
    "female_population": "data/sections_gipuzkoa_demographic_women.geojson",
    "male_population": "path_to_male_population.csv",
    "population_origin": "path_to_population_origin.csv",
    "population_age": "path_to_population_age.csv",
}

# Load the GeoJSON file
geojson_path = "data/aggregated_buildings_multipolygons_sections.geojson"
gdf = gpd.read_file(geojson_path)

# Dash app setup
app = dash.Dash(__name__)
server = app.server

# Serve the GeoJSON file dynamically
@app.server.route('/geojson')
def serve_geojson():
    return jsonify(json.loads(gdf.to_json()))

# Layout with sidebar and map
app.layout = html.Div(
    style={"position": "relative", "height": "100vh"},
    children=[
        # Sidebar
        html.Div(
            id="sidebar",
            style={
                "position": "absolute",
                "top": "20px",
                "left": "20px",
                "width": "300px",
                "backgroundColor": "rgba(255, 255, 255, 0.9)",
                "padding": "15px",
                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",
                "zIndex": 1000,
                "borderRadius": "8px",
            },
            children=[
                html.H3("Demographic Data", style={"marginTop": "0", "fontSize": "18px"}),

                # Dropdown for demographic data selection
                dcc.Dropdown(
                    id="demographic-dropdown",
                    options=[
                        {"label": "Mean Age", "value": "mean_age"},
                        {"label": "Average Income", "value": "average_income"},
                        {"label": "Total Population", "value": "total_population"},
                        {"label": "Female Population", "value": "female_population"},
                        {"label": "Male Population", "value": "male_population"},
                        {"label": "Population by Origin", "value": "population_origin"},
                        {"label": "Population by Age Groups", "value": "population_age"},
                    ],
                    placeholder="Select a demographic variable",
                    multi=False,
                    style={"width": "100%"},
                ),
            ],
        ),

        # Map container
        html.Div(
            id="map-container",
            style={
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "zIndex": 1,
            },
            children=[
                html.Iframe(
                    id="leaflet-map",
                    srcDoc="",  # This will be updated dynamically
                    style={"height": "100%", "width": "100%", "border": "none"},
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("leaflet-map", "srcDoc"),
    Input("demographic-dropdown", "value"),
)
def update_leaflet_map(selected_data):
    if not selected_data:
        # Default empty map
        return """
            <html>
            <head>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
                <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
            </head>
            <body>
                <div id="map" style="height: 100%; width: 100%;"></div>
                <script>
                    var map = L.map('map').setView([43.3, -1.9], 8);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                </script>
            </body>
            </html>
        """

    # Load the selected data
    if selected_data in sociodemographic_files:
        if selected_data.endswith(".geojson"):
            data_gdf = gpd.read_file(sociodemographic_files[selected_data])
        else:
            data_df = pd.read_csv(sociodemographic_files[selected_data])
            data_gdf = gdf.merge(data_df, left_on="CUSEC", right_on="geo_id")

        # Convert to GeoJSON
        data_geojson = data_gdf.to_json()

        # Generate the Leaflet map with choropleth
        leaflet_map = f"""
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
        </head>
        <body>
            <div id="map" style="height: 100%; width: 100%;"></div>
            <script>
                var map = L.map('map').setView([43.3, -1.9], 8);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
                
                var geojsonLayer = L.geoJSON({data_geojson}, {{
                    style: function (feature) {{
                        var value = feature.properties.value;  // Adjust for your property
                        var color = value > 100 ? 'blue' : 
                                    value > 50 ? 'green' : 
                                    'red';  // Adjust color logic
                        return {{color: color, weight: 1}};
                    }},
                    onEachFeature: function (feature, layer) {{
                        layer.bindPopup("Value: " + feature.properties.value);
                    }}
                }}).addTo(map);
            </script>
        </body>
        </html>
        """
        return leaflet_map

    return "Invalid selection."


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

