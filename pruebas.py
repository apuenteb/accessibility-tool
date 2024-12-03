import dash
from dash import html, dcc
import dash_leaflet as dl
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("GeoJSON Example with Dash"),
    
    # Dropdown to choose an option (using dcc.Dropdown instead of dash_leaflet.Dropdown)
    html.Label("Choose an Option:"),
    html.Div([
        dcc.Dropdown(  # Use dcc.Dropdown here
            id='option-dropdown',
            options=[
                {'label': 'Option 1', 'value': 'option1'},
                {'label': 'Option 2', 'value': 'option2'}
            ],
            value='option1'  # Default value
        )
    ], style={'width': '300px', 'margin': '10px'}),
    
    # Map component with a TileLayer for base map and centered view
    dl.Map(
        [ 
            dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", 
                         attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"),
            dl.GeoJSON(id='geojson')  # GeoJSON layer for our feature, with proper ID
        ], 
        id="map", 
        style={'width': '100%', 'height': '500px'}, 
        center=[43.35, -2.05],  # Set the center of the map
        zoom=13  # Set the zoom level
    )
])

# Callback to update GeoJSON data, style and overlay
@app.callback(
    [Output('geojson', 'data'), 
     Output('geojson', 'style_function'),
     Output('map', 'children')],
    [Input('option-dropdown', 'value')]  # Trigger when dropdown changes
)
def update_map(option):
    # Define GeoJSON data
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-2.05, 43.35]
                },
                "properties": {
                    "CUSEC": "654321",
                    "Municipio": "Another Municipio"
                }
            }
        ]
    }

    # Style dictionary instead of function
    geojson_style = {
        'fillColor': 'blue',
        'weight': 1,
        'opacity': 1,
        'color': 'white',
        'dashArray': '3',
        'fillOpacity': 0.6
    }

    # Create a square overlay, color changes based on dropdown option
    if option == 'option1':
        square_color = 'blue'
    elif option == 'option2':
        square_color = 'pink'

    # Define the overlay (rectangle) bounds
    overlay = dl.Rectangle(
        bounds=[[[43.33, -2.08], [43.37, -2.02]]],  # Coordinates for the square's bounds
        color=square_color,  # Color based on selected option
        weight=3,
        opacity=0.6
    )

    # Return the updated GeoJSON data, style, and the overlay
    return geojson_data, geojson_style, [overlay]  # Ensure the overlays are passed as a list

if __name__ == '__main__':
    app.run_server(debug=True)
