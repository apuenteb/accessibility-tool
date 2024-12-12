import dash
from dash import dcc, html, Input, Output, State, _dash_renderer, Dash, callback
from flask import send_file
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

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
app = dash.Dash(external_stylesheets=dmc.styles.ALL)
server = app.server

# Flask route to serve the Leaflet map
@app.server.route('/assets/prueba_map')
def serve_leaflet_map():
    return send_file('assets/prueba_map.html')

# Serve the GeoJSON file
@app.server.route('/geojson')
def serve_geojson_bottom():
    return send_file('data/buildings_by_section.geojson')

# Layout with sidebar over the map
app.layout = html.Div(
    style={"position": "relative", "height": "100vh"},
    children=[
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
                    id="prueba-map",
                    src="/assets/prueba_map",
                    style={"height": "100%", "width": "100%", "border": "none"},
                ),
            ],
        ),

        html.Div(
            style={
                "position": "absolute",
                "top": "10px",
                "left": "10px",
                "width": "350px",
                "backgroundColor": "white",
                "padding": "10px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                "zIndex": 2,  # Ensure it's above the map
            },
            children=[
                dmc.MantineProvider(
                    [
                        dmc.Title("Select the Points of Interest", order=3),
                        dmc.ScrollArea(
                            h=250,
                            w=350,
                            children=dmc.Stack(
                                [
                                    dmc.Checkbox(id="farmacias", checked=False, label="Pharmacies"),
                                    dmc.Checkbox(id="bibliotecas-publicas", checked=False, label="Public libraries"),
                                    dmc.Checkbox(id="colegios", checked=False, label="Schools"),
                                    dmc.Checkbox(id="supermercados", checked=False, label="Supermarkets"),
                                    dmc.Checkbox(id="instalaciones-deportivas", checked=False, label="Sports facilities"),
                                    dmc.Checkbox(id="restaurantes", checked=False, label="Restaurants"),
                                    dmc.Checkbox(id="gym", checked=False, label="Gyms"),
                                    dmc.Checkbox(id="paradas-pt", checked=False, label="Public transport stops"),
                                ]
                            ),
                        ),
                    ]
                )
            ],
        ),
    ],
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
