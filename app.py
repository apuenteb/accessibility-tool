import dash
from dash import html, Input, Output, ALL, callback, ctx, _dash_renderer
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_leaflet as dl
from dash_extensions.javascript import assign

def get_info(feature=None):
    header = [html.H4("Demographic data")]
    if not feature:
        return header + [html.P("Hover over a building")]
    
    # Extract properties from the feature
    municipio = feature["properties"].get("Municipio", "Unknown")
    density_str = feature["properties"].get("density", "N/A")
    
    # Display the information including Municipio and density as strings
    return header + [
        html.B(feature["properties"]["Municipio"]), html.Br(),
        f"Density: {density_str} people / mi²", html.Br(),
        html.B("CUSEC: "), feature["properties"].get("CUSEC", "N/A"), html.Br(),
        html.B("Municipio: "), municipio  # Add Municipio here
    ]

# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"})

# Inline JavaScript for styles when hovering over polygons
visual_style = assign("""
    function(feature) {
        return {
            color: '#3182bd',
            weight: 2,
            opacity: 0.8,
            fillColor: '#6baed6',
            fillOpacity: 0.4
        };
    }
""")

highlight_style = assign("""
    function() {
        return {
            color: '#2b5775',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.7
        };
    }
""")

# Inline JavaScript for hover interaction
on_each_feature = assign("""
    function(feature, layer) {
        // Reference to highlighted layers
        let highlightedLayers = [];

        // Mouseover event
        layer.on('mouseover', function() {
            const CUSEC = feature.properties['CUSEC'];
            
            // Highlight all polygons with the same CUSEC
            this._map.eachLayer((otherLayer) => {
                if (otherLayer.feature && otherLayer.feature.properties['CUSEC'] === CUSEC) {
                    otherLayer.setStyle({
                        color: '#2b5775',
                        weight: 3,
                        opacity: 1,
                        fillOpacity: 0.7
                    });
                    highlightedLayers.push(otherLayer);
                }
            });
        });

        // Mouseout event
        layer.on('mouseout', function() {
            // Reset the style of all highlighted layers
            highlightedLayers.forEach((hlLayer) => {
                hlLayer.setStyle({
                    color: '#3182bd',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: '#6baed6',
                    fillOpacity: 0.4
                });
            });
            highlightedLayers = [];
        });

        // Tooltip
        layer.bindTooltip(
            `<strong>${feature.properties['CUSEC']}</strong><br>Municipio: ${feature.properties['Municipio']}`,
            { permanent: false, direction: 'top' }
        );
    }
""")

# Dash app
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

# Example points for each layer
educational_layers = [
    {"id": "schools", "label": "Schools", "checked": False, "points": [[51.505, -0.09], [51.51, -0.08]]},
    {"id": "libraries", "label": "Libraries", "checked": False, "points": [[51.515, -0.07], [51.52, -0.06]]},
]

# Layout
app.layout = html.Div(
    [
        dl.Map(
            [
                dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', maxZoom=20),
                dl.GeoJSON(
                    id="geojson",
                    url="/assets/buildings_by_section.geojson",  # Replace with your actual endpoint
                    options=dict(style=visual_style, onEachFeature=on_each_feature),
                ),
                dl.LayerGroup(id="map-points"),
            ],
            center=[43.3, -2.0],
            zoom=11,
            style={"height": "100vh", "width": "100%"},
        ),
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
    info
    ]
)

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

# Update the callback to display the hovered feature's information, including CUSEC
@callback(Output("info", "children"), Input("geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)

if __name__ == "__main__":
    app.run_server(debug=True)

