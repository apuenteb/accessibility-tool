import dash
from dash import html, Input, Output, ALL, callback, ctx, _dash_renderer
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_leaflet as dl
from dash_extensions.javascript import assign
import json

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

visual_style = assign("""
    function(feature) {
        return {
            color: '#3182bd',
            weight: 2,
            opacity: 0.8,
            fillColor: feature.properties.color||'#6baed6',
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
        // Mouseover event
        layer.on('mouseover', function() {
            const CUSEC = feature.properties['CUSEC'];

            // Highlight all polygons with the same CUSEC
            this._map.eachLayer((otherLayer) => {
                if (otherLayer.feature && otherLayer.feature.properties['CUSEC'] === CUSEC) {
                    if (!otherLayer.options._originalStyle) {
                        // Save the original style if not already saved
                        otherLayer.options._originalStyle = {
                            color: otherLayer.options.color,
                            weight: otherLayer.options.weight,
                            opacity: otherLayer.options.opacity,
                            fillColor: otherLayer.options.fillColor,
                            fillOpacity: otherLayer.options.fillOpacity,
                        };
                    }
                    otherLayer.setStyle({
                        color: '#2b5775',
                        weight: 3,
                        opacity: 1,
                        fillOpacity: 0.7
                    });
                }
            });
        });

        // Mouseout event
        layer.on('mouseout', function() {
            const CUSEC = feature.properties['CUSEC'];

            // Reset the style of all polygons with the same CUSEC
            this._map.eachLayer((otherLayer) => {
                if (otherLayer.feature && otherLayer.feature.properties['CUSEC'] === CUSEC) {
                    const originalStyle = otherLayer.options._originalStyle;
                    if (originalStyle) {
                        otherLayer.setStyle(originalStyle);
                    }
                }
            });
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

# Load POI GeoJSON files
with open("assets/filtered-centros-educativos.geojson", "r") as f:
    schools_geojson = json.load(f)

with open("assets/filtered-bibliotecas.geojson", "r") as f:
    libraries_geojson = json.load(f)

with open("assets/hospitales.geojson", "r") as f:
    hospitals_geojson = json.load(f)

# Dictionaries by POI categories
educational_layers = [
    {"label": "Schools", "geojson": schools_geojson, "checked": False},
    {"label": "Public libraries", "geojson": libraries_geojson, "checked": False},
    {"label": "Hospitals", "geojson": hospitals_geojson, "checked": False},
]

train_layers = [
    {"label": "Euskotren", "checked": False},
    {"label": "Renfe Cercanías", "checked": False},
]

bus_layers=[
    {"label": "Lurraldebus", "checked": False},
    {"label": "DBus", "checked": False},
]

bike_layers=[
    {"label": "DBizi", "checked": False},
]

poi_menu=html.Div(
            dbc.Accordion(
                [
                    # Educational Section
                    dbc.AccordionItem(
                        dmc.MantineProvider(
                            children=[
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
                            ]
                        ),
                        title="Education",
                        item_id="educational",
                    ),
                    # Transport Section
                    dbc.AccordionItem(
                        dmc.MantineProvider(
                            children=[
                                # Bus
                                html.Div([
                                    dmc.Checkbox(
                                        id="all-bus",
                                        label="Bus",
                                        checked=False,
                                        indeterminate=False
                                    ),
                                    html.Div([
                                        dmc.Checkbox(
                                            id={"type": "bus-item", "index": i},
                                            label=item["label"],
                                            checked=item["checked"],
                                            style={"marginTop": "5px", "marginLeft": "33px"}
                                        )
                                        for i, item in enumerate(bus_layers)
                                    ])
                                ]),
                                # Train
                                html.Div([
                                    dmc.Checkbox(
                                        id="all-train",
                                        label="Train",
                                        checked=False,
                                        indeterminate=False
                                    ),
                                    html.Div([
                                        dmc.Checkbox(
                                            id={"type": "train-item", "index": i},
                                            label=item["label"],
                                            checked=item["checked"],
                                            style={"marginTop": "5px", "marginLeft": "33px"}
                                        )
                                        for i, item in enumerate(train_layers)
                                    ])
                                ]),
                                # Bike
                                html.Div([
                                    dmc.Checkbox(
                                        id="all-bike",
                                        label="Bike",
                                        checked=False,
                                        indeterminate=False
                                    ),
                                    html.Div([
                                        dmc.Checkbox(
                                            id={"type": "bike-item", "index": i},
                                            label=item["label"],
                                            checked=item["checked"],
                                            style={"marginTop": "5px", "marginLeft": "33px"}
                                        )
                                        for i, item in enumerate(bike_layers)
                                    ])
                                ]),
                            ]
                        ),
                        title="Transport",
                        item_id="transport",
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
    )

# Layout
app.layout = html.Div(
    [
        dl.Map(
            [
                dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', maxZoom=20),
                dl.GeoJSON(
                    id="geojson",
                    url="/assets/hospital_with_colors_bike.geojson",  # Replace with your actual endpoint
                    options=dict(style=visual_style, onEachFeature=on_each_feature),
                ),
                dl.LayerGroup(id="map-points"),
            ],
            center=[43.3, -2.0],
            zoom=11,
            style={"height": "100vh", "width": "100%"},
        ),
        poi_menu,
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
def update_main_checkbox_education(all_checked, checked_states):
    # handle "all" checkbox"
    if ctx.triggered_id == 'all-educational':
        checked_states = [all_checked] * len(checked_states)
    # handled individual check boxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

@callback(
    Output("map-points", "children"),
    Input({"type": "educational-item", "index": ALL}, "checked"),
)
def update_map(checked_states):
    map_points = []
    for i, is_checked in enumerate(checked_states):
        if is_checked:
            layer = educational_layers[i]  # Access the layer directly
            for feature in layer["geojson"]["features"]:
                # Check if coordinates are valid (latitude and longitude are not null)
                coordinates = feature.get("geometry", {}).get("coordinates", None)
                if coordinates and len(coordinates) >= 2:
                    lon, lat = coordinates  # Coordinates are [longitude, latitude]
                    if lat is not None and lon is not None:
                        map_points.append(
                            dl.Marker(
                                position=[lat, lon],  # Use [lat, lon] in the correct order
                                children=[dl.Popup(layer["label"])]
                            )
                        )
    return map_points

@callback(
    Output("all-train", "checked"),
    Output("all-train", "indeterminate"),
    Output({"type": "train-item", "index": ALL}, "checked"),
    Input("all-train", "checked"),
    Input({"type": "train-item", "index": ALL}, "checked"),
    prevent_initial_callback=True
)
def update_main_checkbox_train(all_checked, checked_states):
    # handle "all" checkbox"
    if ctx.triggered_id == 'all-train':
        checked_states = [all_checked] * len(checked_states)
    # handled individual check boxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

@callback(
    Output("all-bus", "checked"),
    Output("all-bus", "indeterminate"),
    Output({"type": "bus-item", "index": ALL}, "checked"),
    Input("all-bus", "checked"),
    Input({"type": "bus-item", "index": ALL}, "checked"),
    prevent_initial_callback=True
)
def update_main_checkbox_bus(all_checked, checked_states):
    # handle "all" checkbox"
    if ctx.triggered_id == 'all-bus':
        checked_states = [all_checked] * len(checked_states)
    # handled individual check boxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

@callback(
    Output("all-bike", "checked"),
    Output("all-bike", "indeterminate"),
    Output({"type": "bike-item", "index": ALL}, "checked"),
    Input("all-bike", "checked"),
    Input({"type": "bike-item", "index": ALL}, "checked"),
    prevent_initial_callback=True
)
def update_main_checkbox_bike(all_checked, checked_states):
    # handle "all" checkbox"
    if ctx.triggered_id == 'all-bike':
        checked_states = [all_checked] * len(checked_states)
    # handled individual check boxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

# Update the callback to display the hovered feature's information, including CUSEC
@callback(Output("info", "children"), Input("geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)

if __name__ == "__main__":
    app.run_server(debug=True)
