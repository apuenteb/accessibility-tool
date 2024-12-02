import dash
from dash import dcc, html, Input, Output
from flask import send_file

sociodemographic_files = {
    "mean_age": "path_to_mean_age.csv",
    "average_income": "path_to_average_income.csv",
    "total_population": "path_to_total_population.csv",
    "female_population": "section_gipuzkoa_demographic_women.geojson",
    "male_population": "path_to_male_population.csv",
    "population_origin": "path_to_population_origin.csv",
    "population_age": "path_to_population_age.csv",
}

# Dash app
app = dash.Dash(__name__)

# Serve the HTML template directly
@app.server.route('/leaflet_map')
def serve_leaflet_map():
    return send_file('leaflet_map.html')

# Serve the GeoJSON file
@app.server.route('/geojson')
def serve_geojson():
    return send_file('aggregated_buildings_multipolygons_sections.geojson')

# Layout with sidebar and map
app.layout = html.Div(
    children=[
        # Sidebar (floating on top of the map)
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
                "zIndex": 1000,  # Ensures it stays on top of the map
                "borderRadius": "8px",
            },
            children=[
                html.H3("Demographic Data", style={"marginTop": "0", "fontSize": "18px"}),

                # Dropdown to select demographic data
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

                # Placeholder for file inputs
                html.Div(id="file-input-container", children=[]),
            ],
        ),

        # Map container (Iframe)
        html.Div(
            children=[
                html.Iframe(
                    src="/leaflet_map",  # Assuming the map is being served here
                    style={"height": "100vh", "width": "100vw", "border": "none"},
                )
            ]
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False)


