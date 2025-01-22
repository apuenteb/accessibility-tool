import dash
from dash import Dash, html, dcc, _dash_renderer
from dash.dependencies import Input, Output
import dash_leaflet as dl
from dash_extensions.javascript import assign
import json
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc  # For advanced styling

# Inline JavaScript for styling with dynamic clicked state
visual_style = assign(""" 
    function(feature) {
        const isClicked = feature.properties.clicked || false;
        const selectedColor = feature.properties.selectedColor || '#6baed6'; // Default color (blue)
        return {
            color: '#3182bd',
            weight: 2,
            opacity: 0.8,
            fillColor: selectedColor,
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
                fillColor: feature.properties.selectedColor || '#6baed6', // Default fill color (blue)
                fillOpacity: 0.4
            });
        });
    }
""")

# Load US states GeoJSON data
with open("./assets/states_colored.geojson") as f:
    us_states_geojson = json.load(f)

# Initialize clicked state for each feature and set the initial selected color to blue
for feature in us_states_geojson['features']:
    feature['properties']['selectedColor'] = '#6baed6'  # Default color (blue)

# Dash app
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

@app.callback(
    Output('states-layer', 'data'),
    [Input('color-checklist', 'value')]
)
def update_color(selected_colors):
    # Update the selected colors based on checklist input
    for feature in us_states_geojson['features']:
        # If no colors are selected, set the color to default (blue)
        if not selected_colors:
            feature['properties']['selectedColor'] = '#6baed6'  # Default to blue
        else:
            # Set color based on selected options
            if 'color_1' in selected_colors:
                feature['properties']['selectedColor'] = feature['properties']['color_1']
            elif 'color_2' in selected_colors:
                feature['properties']['selectedColor'] = feature['properties']['color_2']
    
    return us_states_geojson

# Create the color menu and layers
color_layers_menu = html.Div(
    dbc.Accordion(
        [
            # Color Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[   
                        # Checklist for color selection, with no default value selected
                        dcc.Checklist(
                            id='color-checklist',
                            options=[
                                {'label': 'Color 1', 'value': 'color_1'},
                                {'label': 'Color 2', 'value': 'color_2'},
                            ],
                            value=[],  # No color selected by default
                            labelStyle={'display': 'block', 'marginLeft': '20px'}
                        )
                    ]
                ),
                title="Color Selection",
                item_id="color-selection",
            ),
        ],
        id="accordion",
        active_item="color-selection",
    ),
    style={
        "position": "absolute",
        "top": "10px",
        "left": "10px",
        "zIndex": "1000",
        "backgroundColor": "rgba(255, 255, 255, 0.9)",
        "padding": "10px",
        "borderRadius": "5px",
        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
        "width": "250px",
    },
)

app.layout = html.Div([
    # Menu section with the color layers
    color_layers_menu,
    
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
