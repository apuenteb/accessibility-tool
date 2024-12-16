import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_leaflet as dl
import json

# Initialize the Dash app
app = dash.Dash(__name__)

# Load GeoJSON data
with open("assets/filtered-centros-educativos.geojson", "r") as f:
    schools_geojson = json.load(f)

with open("assets/filtered-bibliotecas.geojson", "r") as f:
    libraries_geojson = json.load(f)

# Create a dictionary to map checkboxes to GeoJSON data
layers = {
    "Schools": schools_geojson,
    "Bibliotecas": libraries_geojson,
}

# Layout
app.layout = html.Div([
    dcc.Checklist(
        id="layer-checklist",
        options=[{"label": name, "value": name} for name in layers.keys()],
        value=[],  # Start with no layers selected
        inline=True
    ),
    dl.Map([
        dl.TileLayer(),
        dl.LayerGroup(id="layer-group")  # Placeholder for dynamic layers
    ], center=(43.3, -2.0), zoom=11, style={"height": "80vh", "width": "100%"}),
])

# Callback to update map layers
@app.callback(
    Output("layer-group", "children"),
    Input("layer-checklist", "value")
)
def update_layers(selected_layers):
    # Generate a list of GeoJSON layers for selected checkboxes
    return [dl.GeoJSON(data=layers[layer], id=f"{layer.lower()}-layer") for layer in selected_layers]   

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)