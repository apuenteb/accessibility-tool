import dash
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, _dash_renderer, Dash, callback
import dash_leaflet as dl

_dash_renderer._set_react_version("18.2.0")

# Initialize Dash app
app = dash.Dash(external_stylesheets=dmc.styles.ALL)

# Layout with MantineProvider wrapping the components
app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        html.Div(
            id="checklist-container",
            children=[
                dmc.CheckboxGroup(
                    id="layer-checklist",
                    value=[],  # Start with no layers selected
                    children=[
                        html.Div([
                            dmc.Checkbox(
                                id="educational-group",
                                label="Educational",
                            ),
                            dmc.Group(
                                children=[
                                    dmc.Checkbox(label="Schools", value="Schools"),
                                ],
                                style={"marginLeft": "20px"}
                            )
                        ]),
                        html.Div([
                            dmc.Checkbox(
                                id="cultural-group",
                                label="Cultural",
                            ),
                            dmc.Group(
                                children=[
                                    dmc.Checkbox(label="Libraries", value="Libraries"),
                                ],
                                style={"marginLeft": "20px"}
                            )
                        ])
                    ]
                )
            ],
            style={"width": "300px", "padding": "10px", "backgroundColor": "white"}
        ),

        # Dash Leaflet Map
        dl.Map(
            [
                dl.TileLayer(),
                dl.LayerGroup(id="layer-group")  # Placeholder for dynamic layers
            ],
            center=(43.3, -2.0),
            zoom=11,
            style={"height": "80vh", "width": "100%"}
        )
    ]
)

# Callback to update map layers based on checkbox selection
@app.callback(
    Output("layer-group", "children"),
    [Input("educational-group", "value"),
     Input("cultural-group", "value")]
)
def update_map_layers(educational, cultural):
    # Ensure that educational and cultural values are lists (default to empty list)
    educational = educational or []
    cultural = cultural or []

    layers = []
    
    # Check if "Schools" is selected
    if "Schools" in educational:
        layers.append(dl.Marker(position=(43.3, -2.0), children=dl.Popup("School")))
    
    # Check if "Libraries" is selected
    if "Libraries" in cultural:
        layers.append(dl.Marker(position=(43.3, -2.5), children=dl.Popup("Library")))
    
    return layers

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)



