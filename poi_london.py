import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, Input, Output, ALL, callback, ctx, _dash_renderer
import dash_leaflet as dl
from dash_extensions.javascript import arrow_function

################################################## SETUP ################################################################
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

######################################### INITIALIZATION OF VARIABLES ################################################################
# Example points for each layer
educational_layers = [
    {"id": "schools", "label": "Schools", "checked": False, "points": [[51.505, -0.09], [51.51, -0.08]]},
    {"id": "libraries", "label": "Libraries", "checked": False, "points": [[51.515, -0.07], [51.52, -0.06]]},
]


style_handle = {
    "color": "blue",
    "weight": 2,
    "fillColor": "blue",
    "fillOpacity": 0.4
}

hover_style = {
    "weight": 5,
    "color": '#666',
    "dashArray": ''
}

geojson = dl.GeoJSON(
    url="/assets/sections_gipuzkoa.geojson",  # Adjust the path to your GeoJSON file
    style=style_handle,  # Styling for the polygons
    zoomToBounds=True,  # Auto zoom to bounds when data is loaded
    zoomToBoundsOnClick=True,  # Zoom to polygon bounds on click
    hoverStyle=hover_style,  # Hover styling
    onEachFeature="""
        function(feature, layer) {
            layer.on('mouseover', function() {
                layer.setStyle({weight: 5, color: '#666', dashArray: ''});
            });
            layer.on('mouseout', function() {
                layer.setStyle({weight: 2, color: 'white', dashArray: '3'});
            });
        }
    """,
    id="geojson"
)

################################################## LAYOUT ################################################################
app.layout = html.Div([
    html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    dmc.MantineProvider(
                        children=html.Div([

                            dmc.Checkbox(
                                id="all-educational",
                                label="Educational",
                                checked=False,
                                indeterminate=False
                            ), 

                            html.Div([

                                dmc.Checkbox(
                                    id={"type": "educational-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )

                                for i, item in enumerate(educational_layers)
                            ])
                        ])
                    ),
                    title="Educational Layers",
                    item_id="educational",
                ),
            ],
            id="accordion",
            active_item="educational",
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
    ),
    dl.Map(
        [
            dl.TileLayer(),
            dl.LayerGroup(id="map-points"),
            geojson
        ],
        center=[51.505, -0.09],
        zoom=13,
        style={"height": "100vh", "width": "100%"},
    ),
])



############################################### CALLBACKS ################################################################
@callback(
    Output("all-educational", "checked"),
    Output("all-educational", "indeterminate"),
    Output({"type": "educational-item", "index": ALL}, "checked"),
    Input("all-educational", "checked"),
    Input({"type": "educational-item", "index": ALL}, "checked"),
    prevent_initial_callback=True
)
def update_educational_checkbox(all_checked, checked_states):
    # Handle parent checkbox
    if ctx.triggered_id == 'all-educational':
        checked_states = [all_checked] * len(checked_states)

    # Handle child checkboxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states


@callback(
    Output("map-points", "children"),
    Input({"type": "educational-item", "index": ALL}, "checked"),
)
def update_map(checked_states):
    # Add points to the map based on checked layers
    map_points = []
    for i, is_checked in enumerate(checked_states):
        if is_checked:
            layer = educational_layers[i]
            layer_points = [
                dl.Marker(position=point, children=[dl.Popup(layer["label"])])
                for point in layer["points"]
            ]

            map_points.extend(layer_points)
    return map_points


################################################## RUN ################################################################
if __name__ == '__main__':
    app.run_server(debug=True)

