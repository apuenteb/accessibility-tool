import dash
from dash import dcc, html, Input, Output, State
from flask import send_file
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px

# File paths for demographic data
sociodemographic_files = {
    "mean_age": "path_to_mean_age.csv",
    "average_income": "path_to_average_income.csv",
    "total_population": "path_to_total_population.csv",
    "female_population": "section_gipuzkoa_demographic_women.geojson",
    "male_population": "path_to_male_population.csv",
    "population_origin": "path_to_population_origin.csv",
    "population_age": "path_to_population_age.csv",
}

# Dash app setup
app = dash.Dash(__name__)
server = app.server

# Flask route to serve the Leaflet map
@app.server.route('/assets/leaflet_map')
def serve_leaflet_map():
    return send_file('assets/leaflet_map.html')

# Serve the GeoJSON file
@app.server.route('/geojson')
def serve_geojson():
    return send_file('data/aggregated_buildings_multipolygons_sections.geojson')

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
                    src="/assets/leaflet_map",
                    style={"height": "100%", "width": "100%", "border": "none"},
                ),
                html.Div(
                    id="map-overlay",
                    style={"display": "none"},  # Will display dynamically
                ),
            ],
        ),
    ],
)

# Callback to display demographic data on the map
@app.callback(
    Output("map-overlay", "children"),
    Output("map-overlay", "style"),
    Input("demographic-dropdown", "value"),
)
def update_map_overlay(selected_data):
    if not selected_data:
        return None, {"display": "none"}

    # Get the file path for the selected data
    file_path = sociodemographic_files[selected_data]

    # Load data (CSV or GeoJSON)
    if file_path.endswith(".geojson"):
        df = gpd.read_file(file_path)
    else:
        df = pd.read_csv(file_path)

    # Ensure the necessary columns are present
    if "geo_id" not in df.columns or "value" not in df.columns:
        return html.Div(f"Invalid data format for {selected_data}."), {"display": "none"}

    # Create a choropleth map
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="geo_id",  # Matches GeoJSON feature ID
        color="value",  # Column to color by
        color_continuous_scale="Viridis",
        title=f"Demographic Data: {selected_data.replace('_', ' ').title()}",
        mapbox_style="carto-positron",
        hover_name="geo_id",
        center={"lat": 40, "lon": -3},  # Adjust as needed
        zoom=6,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Display the graph as an overlay
    return dcc.Graph(figure=fig), {"position": "absolute", "top": "0", "left": "0", "right": "0", "bottom": "0", "zIndex": 2}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
