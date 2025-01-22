import dash
from dash import Dash, html, dcc, _dash_renderer, ALL, ctx, callback
from dash.dependencies import Input, Output, State
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

# Dictionaries by POI categories
color_layers = [
    {"label": "Color 1", "value": "color_1", "checked": False},
    {"label": "Color 2", "value": "color_2", "checked": False},
    {"label": "Color 3", "value": "color_3", "checked": False},
]

# Dash app
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

@app.callback(
    Output('states-layer', 'data'),
    [Input({"type": "color-item", "index": ALL}, "checked")]  # Listen for changes in the checked state of the color checkboxes
)
def update_color(checked_values):
    # Update the selected colors based on checkbox input (checked state)
    selected_colors = []

    # Iterate over the checked values to gather the selected colors
    for idx, checked in enumerate(checked_values):
        if checked:  # If the checkbox is checked
            selected_colors.append(color_layers[idx]["value"])  # Get the value of the selected color

    # Update the GeoJSON based on the selected colors
    for feature in us_states_geojson['features']:
        if selected_colors:
            # Assign a color based on the selected colors
            if 'color_1' in selected_colors:
                feature['properties']['selectedColor'] = feature['properties']['color_1']  # Use color_1 from GeoJSON
            elif 'color_2' in selected_colors:
                feature['properties']['selectedColor'] = feature['properties']['color_2']  # Use color_2 from GeoJSON
            elif 'color_3' in selected_colors:
                feature['properties']['selectedColor'] = '#0000ff'  # Example: blue for color_3
        else:
            # If no colors are selected, revert to the default color (blue)
            feature['properties']['selectedColor'] = '#6baed6'  # Default to blue

    return us_states_geojson  # Return the updated GeoJSON data

# Create the color menu and layers
color_layers_menu = html.Div(
    dbc.Accordion(
        [
            # Color Section
            dbc.AccordionItem(
                        dmc.MantineProvider(
                            children=[
                                dmc.Checkbox(
                                    id="all-colors",
                                    label="Colors",
                                    checked=False,
                                    indeterminate=False
                                ),
                                html.Div([ 
                                    dmc.Checkbox(
                                        id={"type": "color-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(color_layers)
                                ])
                            ]
                        ),
                        title="Color Selection",
                        item_id="colors",
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

@callback(
    Output("all-colors", "checked"),
    Output("all-colors", "indeterminate"),
    Output({"type": "color-item", "index": ALL}, "checked"),
    Input("all-colors", "checked"),
    Input({"type": "color-item", "index": ALL}, "checked"),
    prevent_initial_callback=True
)
def update_main_checkbox_colors(all_checked, checked_states):
    # handle "all" checkbox
    if ctx.triggered_id == 'all-colors':
        checked_states = [all_checked] * len(checked_states)
    # handle individual checkboxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

if __name__ == "__main__":
    app.run_server(debug=True)
