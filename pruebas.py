import dash_bootstrap_components as dbc
import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, ALL, callback, ctx, _dash_renderer
from flask import send_file

################################################## SETUP ################################################################
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

######################################### INITIALIZATION OF VARIABLES ################################################################
educational_layers = [
    {"id": "schools", "label": "Schools", "checked": False},
    {"id": "libraries", "label": "Libraries", "checked": False},
]


# Flask route to serve the Leaflet map
@app.server.route('/assets/prueba_map')
def serve_leaflet_map():
    return send_file('assets/prueba_map.html')

# Serve the GeoJSON file
@app.server.route('/geojson')
def serve_geojson_bottom():
    return send_file('data/buildings_by_section.geojson')

################################################## LAYOUT ################################################################
app.layout = html.Div(
    [
        # Floating menu
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
                                    indeterminate=False,
                                ),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "educational-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"},
                                    )
                                    for i, item in enumerate(educational_layers)
                                ]),
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
        # Map container
        html.Div(
            id="map-container",
            style={
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "zIndex": 1,
            },
            children=[
                html.Iframe(
                    id="prueba-map",
                    src="/assets/prueba_map",
                    style={"height": "100%", "width": "100%", "border": "none"},
                ),
            ],
        ),
    ]
)

################################################## CALLBACKS ################################################################
@callback(
    Output("all-educational", "checked"),
    Output("all-educational", "indeterminate"),
    Output({"type": "educational-item", "index": ALL}, "checked"),
    Input("all-educational", "checked"),
    Input({"type": "educational-item", "index": ALL}, "checked"),
    prevent_initial_callback=True,
)
def update_educational_checkbox(all_checked, checked_states):
    if ctx.triggered_id == "all-educational":
        checked_states = [all_checked] * len(checked_states)

    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

################################################## RUN ################################################################
if __name__ == "__main__":
    app.run_server(debug=True)
