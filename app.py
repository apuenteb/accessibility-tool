import dash
from dash import dcc, html, Input, Output
from flask import send_file
import pandas as pd  # Add this line
import json
import plotly.express as px

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
@app.server.route('leaflet_map')
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

# Callback to update the map based on dropdown selection
@app.callback(
    Output("map-graph", "figure"),
    Input("demographic-dropdown", "value"),
)
def update_map(selected_data):
    if not selected_data:
        # Default placeholder if no option is selected
        return px.choropleth_mapbox(
            pd.DataFrame({"geo_id": [], "value": []}),
            geojson=geojson,
            locations="geo_id",
            color="value",
            title="Select a demographic variable to view data.",
            height=600,
        ).update_layout(mapbox_style="carto-positron")

    # Load data for the selected option
    file_path = data_files[selected_data]
    df = pd.read_csv(file_path)  # Replace with your actual data loading logic

    # Ensure your dataset contains `geo_id` (or equivalent) matching the GeoJSON
    if "geo_id" not in df or "value" not in df:
        raise ValueError(f"Data for {selected_data} must include 'geo_id' and 'value' columns.")

    # Create a choropleth map
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations="geo_id",  # Match with GeoJSON feature id
        color="value",  # The column to represent
        color_continuous_scale="Viridis",  # Customize the color scale
        title=f"Demographic Data: {selected_data.replace('_', ' ').title()}",
        mapbox_style="carto-positron",
        hover_name="geo_id",  # Replace with a column for hover information
        center={"lat": 40, "lon": -3},  # Center the map (adjust lat/lon)
        zoom=6,  # Adjust the zoom level
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)


