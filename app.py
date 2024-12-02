import dash
from dash import dcc, html, Input, Output
from flask import send_file
import geopandas as gpd
import json
from dash.exceptions import PreventUpdate

# Load GeoJSON data and prepare demographic options
sections = gpd.read_file('aggregated_buildings_multipolygons_sections.geojson')
geojson_data = json.loads(sections.to_json())

# Extract demographic data columns (assuming they exist in your GeoDataFrame)
demographic_columns = [col for col in sections.columns if col not in ['geometry', 'CUSEC', 'Municipio']]

# Dash app
app = dash.Dash(__name__)

# Serve the HTML template directly
@app.server.route('/leaflet_map')
def serve_leaflet_map():
    return send_file('leaflet_map.html')

# Layout
app.layout = html.Div(
    children=[
        # Floating sidebar with multiple choice options
        html.Div(
            id="sidebar",
            style={
                "position": "absolute",
                "top": "10px",
                "left": "10px",
                "width": "300px",
                "backgroundColor": "rgba(255, 255, 255, 0.9)",
                "padding": "15px",
                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",
                "zIndex": 1000,  # Ensures it stays on top of the map
                "borderRadius": "8px",
            },
            children=[
                html.H3("Demographic Data", style={"marginTop": "0", "fontSize": "18px"}),
                
                # Dropdown to select demographic data with custom labels and values
                dcc.Dropdown(
                    id="demographic-dropdown",
                    options=[
                        {"label": "Population Density", "value": "population_density"},
                        {"label": "Average Income", "value": "average_income"},
                        {"label": "Total Population", "value": "total_population"},
                        {"label": "Housing Quality", "value": "housing_quality"}
                    ],
                    placeholder="Select a demographic?????",
                    multi=False,
                    style={"width": "100%"},
                ),
                
                # Placeholder for file inputs
                html.Div(id="file-input-container", children=[]),
            ],
        ),
        
        # Map container
        html.Div(
            children=[
                html.Iframe(
                    src="/leaflet_map",
                    id="map-frame",
                    style={"height": "100vh", "width": "100vw", "border": "none"},
                )
            ]
        ),
    ]
)

# Callback to dynamically update the file input fields based on dropdown selection
@app.callback(
    Output("file-input-container", "children"),
    [Input("demographic-dropdown", "value")]
)
def update_file_input(selected_data):
    if not selected_data:
        raise PreventUpdate

    # Customizing the file input based on the selected option
    file_input = html.Div(
        [
            html.Label(f"Upload file for {selected_data.replace('_', ' ').title()}:"), 
            dcc.Upload(
                id=f"upload-{selected_data}",
                children=html.Button("Upload File"),
                multiple=False,  # Set to True for multiple files
            ),
            html.Br(),
            html.Div(id=f"file-name-{selected_data}"),  # Dynamically generated ID
        ]
    )
    return file_input

# Callback to display the name of the uploaded file dynamically based on selected data
@app.callback(
    Output("file-name-population_density", "children"),
    Output("file-name-average_income", "children"),
    Output("file-name-total_population", "children"),
    Output("file-name-housing_quality", "children"),
    [Input("upload-population_density", "filename"),
     Input("upload-average_income", "filename"),
     Input("upload-total_population", "filename"),
     Input("upload-housing_quality", "filename")]
)
def update_file_name(population_density_file, average_income_file, total_population_file, housing_quality_file):
    # Handle file name display dynamically based on the selected dropdown option
    if population_density_file:
        return f"File {population_density_file} uploaded successfully", "", "", ""
    if average_income_file:
        return "", f"File {average_income_file} uploaded successfully", "", ""
    if total_population_file:
        return "", "", f"File {total_population_file} uploaded successfully", ""
    if housing_quality_file:
        return "", "", "", f"File {housing_quality_file} uploaded successfully"
    return "", "", "", ""  # Default empty return if no file is uploaded

if __name__ == '__main__':
    app.run_server(debug=True)

