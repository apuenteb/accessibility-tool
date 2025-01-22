from dash import Dash, html, dcc
from dash.dependencies import Input, Output  # Correct import
import dash_leaflet as dl
from dash_extensions.javascript import assign
import json

# Inline JavaScript for styling with dynamic clicked state
visual_style = assign(""" 
    function(feature) {
        const isClicked = feature.properties.clicked || false;
        const selectedColor = feature.properties.selectedColor || '#6baed6'; // Default color
        return {
            color: '#3182bd',
            weight: 2,
            opacity: 0.8,
            fillColor: isClicked ? '#ff0000' : selectedColor,
            fillOpacity: 0.4
        };
    }
""")

# Inline JavaScript for hover and click interaction
on_each_feature = assign(""" 
    function(feature, layer) {
        // Tooltip with state name
        layer.bindTooltip(`<strong>${feature.properties['NAME']}</strong>`, {sticky: true});

        // Mouseover event to highlight the state
        layer.on('mouseover', function() {
            layer.setStyle({
                color: '#ff7800',
                weight: 5,
                fillOpacity: 0.9
            });
        });

        // Mouseout event to reset style
        layer.on('mouseout', function() {
            layer.setStyle({
                color: '#3182bd',
                weight: 2,
                opacity: 0.8,
                fillColor: feature.properties.selectedColor || '#6baed6', // Default fill color
                fillOpacity: 0.4
            });
        });

        // Click event to change fillColor to red and log the state name
        layer.on('click', function() {
            feature.properties.clicked = !feature.properties.clicked; // Toggle clicked state
            layer.setStyle({
                fillColor: feature.properties.clicked ? '#ff0000' : feature.properties.selectedColor, // Toggle color
                weight: 5,
                fillOpacity: 0.9
            });
            console.log('Clicked state: ' + feature.properties['NAME']);
        });
    }
""")

# Load US states GeoJSON data
with open("./assets/states_colored.geojson") as f:
    us_states_geojson = json.load(f)

# Initialize clicked state for each feature and set the initial selected color
for feature in us_states_geojson['features']:
    feature['properties']['clicked'] = False  # Add a 'clicked' property
    feature['properties']['selectedColor'] = feature['properties']['color_1']  # Default to color_1

# Create Dash app
app = Dash(__name__)

@app.callback(
    Output('states-layer', 'data'),
    [Input('menu-dropdown', 'value')]
)
def update_color(selected_color):
    # Update the selected color based on dropdown selection
    for feature in us_states_geojson['features']:
        if selected_color == 'c1':
            feature['properties']['selectedColor'] = feature['properties']['color_1']
        elif selected_color == 'c2':
            feature['properties']['selectedColor'] = feature['properties']['color_2']
    
    return us_states_geojson

app.layout = html.Div([
    # Menu section
    html.Div([
        dcc.Dropdown(
            id='menu-dropdown',
            options=[
                {'label': 'Color 1', 'value': 'c1'},
                {'label': 'Color 2', 'value': 'c2'},
            ],
            value='c1',  # Default value (color_1)
            style={'width': '200px', 'padding': '10px'}
        )
    ], style={'position': 'absolute', 'top': '10px', 'left': '10px', 'zIndex': 999, 'background-color': 'white', 'padding': '10px'}),
    
    # Map Section
    dl.Map([
        dl.TileLayer(),
        dl.GeoJSON(
            id="states-layer",
            data=us_states_geojson,
            options=dict(style=visual_style, onEachFeature=on_each_feature),
        )
    ], 
    style={'width': '100%', 'height': '100vh'},
    center=[39, -98],  # Center on the US
    zoom=4,             # Zoom level
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)
