import dash
from dash import html, dcc, Input, Output, _dash_renderer
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_mantine_components as dmc
import json

# App setup
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

# Example GeoJSON data
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"CUSEC": "001", "Municipio": "London"},
            "geometry": {"type": "Polygon", "coordinates": [[[-0.09, 51.505], [-0.08, 51.505], [-0.08, 51.515], [-0.09, 51.515], [-0.09, 51.505]]]},
        },
        {
            "type": "Feature",
            "properties": {"CUSEC": "002", "Municipio": "Westminster"},
            "geometry": {"type": "Polygon", "coordinates": [[[-0.1, 51.51], [-0.09, 51.51], [-0.09, 51.52], [-0.1, 51.52], [-0.1, 51.51]]]},
        },
    ],
}

# GeoJSON visual style
default_style = {"color": "#3182bd", "weight": 2, "opacity": 0.8, "fillColor": "#6baed6", "fillOpacity": 0.4}
highlight_style = {"color": "#2b5775", "weight": 3, "opacity": 1, "fillOpacity": 0.7}

# App layout
app.layout = html.Div([
    dcc.Store(id="geojson-data", data=geojson_data),
    html.Div(
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    dmc.MantineProvider(
                        children=html.Div([
                            dmc.Checkbox(
                                id="educational-checkbox",
                                label="Educational Points",
                                checked=False
                            ),
                        ])
                    ),
                    title="Map Layers",
                    item_id="layers",
                ),
            ],
            id="accordion",
            active_item="layers",
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
            dl.GeoJSON(
                id="geojson-layer",
                data=geojson_data,
                zoomToBounds=True,
                options=dict(style=default_style),
            ),
        ],
        center=[51.505, -0.09],
        zoom=13,
        style={"height": "100vh", "width": "100%"},
    ),
])

# Callbacks
@app.callback(
    Output("geojson-layer", "hover_style"),
    Input("geojson-layer", "hover_feature"),
)
def highlight_feature(feature):
    """Highlight polygons on hover."""
    if feature:
        return highlight_style
    return default_style

@app.callback(
    Output("geojson-layer", "hideout"),
    Input("educational-checkbox", "checked"),
)
def toggle_layer_visibility(checked):
    """Toggle visibility of GeoJSON layer."""
    return {"display": "block" if checked else "none"}


# Run server
if __name__ == "__main__":
    app.run_server(debug=True)

