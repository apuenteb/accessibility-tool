from dash import Dash, html
import dash_leaflet as dl
from dash_extensions.javascript import assign
import json

# Inline JavaScript for styling with dynamic clicked state
visual_style = assign("""
    function(feature) {
        const isClicked = feature.properties.clicked || false;
        return {
            color: '#3182bd',
            weight: 2,
            opacity: 0.8,
            fillColor: isClicked ? '#ff0000' : '#6baed6',
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
                fillColor: feature.properties.clicked ? '#ff0000' : '#6baed6',
                fillOpacity: 0.4
            });
        });

        // Click event to change fillColor to red and log the state name
        layer.on('click', function() {
            feature.properties.clicked = !feature.properties.clicked; // Toggle clicked state
            layer.setStyle({
                fillColor: feature.properties.clicked ? '#ff0000' : '#6baed6', // Toggle color
                weight: 5,
                fillOpacity: 0.9
            });
            console.log('Clicked state: ' + feature.properties['NAME']);
        });
    }
""")

# Load US states GeoJSON data
with open("./assets/states.geojson") as f:
    us_states_geojson = json.load(f)

# Initialize clicked state for each feature
for feature in us_states_geojson['features']:
    feature['properties']['clicked'] = False  # Add a 'clicked' property

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
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

