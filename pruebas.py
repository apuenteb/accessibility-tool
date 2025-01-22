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

# Load geojson polygons
with open("assets/hospital_with_colors.geojson", "r") as f:
    geojson = json.load(f)

# Set the initial selected color to blue (default)
for feature in geojson['features']:
    feature['properties']['selectedColor'] = '#6baed6'  # Default color (blue)

# Load POI GeoJSON files
with open("assets/filtered-centros-educativos.geojson", "r") as f:
    schools_geojson = json.load(f)

with open("assets/filtered-bibliotecas.geojson", "r") as f:
    libraries_geojson = json.load(f)

with open("assets/hospitales.geojson", "r") as f:
    hospitals_geojson = json.load(f)

# Dictionaries by POI categories
eat_layers = [
    {"label": "Special Food Services", "value": "color_1", "geojson": schools_geojson, "checked": False},
    {"label": "Restaurants", "value": "color_2", "geojson": libraries_geojson, "checked": False},
    {"label": "Cafes & bakeries", "value": "color_3","geojson": hospitals_geojson, "checked": False},
    {"label": "Bars", "value": "color_4","geojson": hospitals_geojson, "checked": False},
]

healthcare_layers = [
    {"label": "Clinics & local healthcare centers", "checked": False},
    {"label": "Hospitals", "checked": False},
    {"label": "Nursing & Residential Care", "checked": False},
    {"label": "Dentists", "checked": False},
    {"label": "Psychologist", "checked": False},
]

leisure_layers = [
    {"label": "Hairdresser & Barbery", "checked": False},
    {"label": "Personal Wellness", "checked": False},
]

professional_layers = [
    {"label": "Administrative and Support Services", "checked": False},
    {"label": "Finance", "checked": False},
    {"label": "Insurance Agency", "checked": False},
    {"label": "Management of Companies", "checked": False},
    {"label": "Professional Services", "checked": False},
    {"label": "Real Estate", "checked": False},
    {"label": "Travel Agency", "checked": False},
]

pharmacy_layers = [
    {"label": "Pharmacy", "checked": False},
]

service_layers = [
    {"label": "Car Rental", "checked": False},
    {"label": "Car Repair", "checked": False},
    {"label": "Death Care Services", "checked": False},
    {"label": "Fuel Station", "checked": False},
    {"label": "Laundry", "checked": False},
    {"label": "Locksmith Errands", "checked": False},
    {"label": "Moving Company", "checked": False},
    {"label": "Parking", "checked": False},
    {"label": "Post Office", "checked": False},
    {"label": "Storage", "checked": False},
    {"label": "Veterinary Services", "checked": False},
    {"label": "Waste Management", "checked": False},
]

hotel_layers = [
    {"label": "Hotel and Lodging", "checked": False},
]

consumergoods_layers = [
    {"label": "Book Store", "checked": False},
    {"label": "Clothing Store", "checked": False},
    {"label": "Cosmetics Retail", "checked": False},
    {"label": "Department Store", "checked": False},
    {"label": "Florist", "checked": False},
    {"label": "Gift and Souvenir", "checked": False},
    {"label": "Hobby Retailers", "checked": False},
    {"label": "Jewelry Stores", "checked": False},
    {"label": "Optical Goods", "checked": False},
    {"label": "Pet Store", "checked": False},
    {"label": "Shoe Store", "checked": False},
    {"label": "Used Merchandise", "checked": False},
    {"label": "Warehouse", "checked": False},
]

durablegoods_layers = [
    {"label": "Car Dealer", "checked": False},
    {"label": "Home Goods Store", "checked": False},
    {"label": "Wholesale Trade", "checked": False},
]

grocery_layers = [
    {"label": "Convenience Corner Store", "checked": False},
    {"label": "Grocery or Supermarket", "checked": False},
    {"label": "Liquor Store", "checked": False},
    {"label": "Specialty Food Retailers", "checked": False},
]

cultural_layers = [
    {"label": "Art Gallery", "checked": False},
    {"label": "Library", "checked": False},
    {"label": "Museum", "checked": False},
]

entertainment_layers = [
    {"label": "Amusement Park", "checked": False},
    {"label": "Bowling", "checked": False},
    {"label": "Casino", "checked": False},
    {"label": "Movie Theater", "checked": False},
    {"label": "Performing Arts", "checked": False},
    {"label": "Spectator Sports", "checked": False},
    {"label": "Zoos and Nature Parks", "checked": False},
]

leisurewellness_layers = [
    {"label": "Golf Courses", "checked": False},
    {"label": "Gym", "checked": False},
    {"label": "Marinas", "checked": False},
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

religious_layers = [
    {"label": "Religious Centers", "checked": False},
]

poi_menu = html.Div(
    dbc.Accordion(
        [
            # Eat Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        html.H6("Food & Beverage", style={"marginTop": "10px", "marginBottom": "5px"}),
                        html.Div([
                            dmc.Checkbox(
                                id={"type": "eat-item", "index": i},
                                label=item["label"],
                                checked=item["checked"],
                                style={"marginTop": "5px", "marginLeft": "10px"}
                            )
                            for i, item in enumerate(eat_layers)
                        ])
                    ]
                ),
                title="Eat",
                item_id="eatery",
            ),
            # Errands Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        # Healthcare
                        html.Div([
                            html.H6("Healthcare", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "healthcare-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(healthcare_layers)
                            ])
                        ]),
                        # Leisure
                        html.Div([
                            html.H6("Leisure & Wellness", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "leisure-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(leisure_layers)
                            ])
                        ]),
                        # Professional Services
                        html.Div([
                            html.H6("Professional Services", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "professional-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(professional_layers)
                            ])
                        ]),
                        # Retail (Pharmacy)
                        html.Div([
                            html.H6("Retail (Pharmacy)", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "pharmacy-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(pharmacy_layers)
                            ])
                        ]),
                        # Service
                        html.Div([
                            html.H6("Service", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "service-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(service_layers)
                            ])
                        ]),
                    ]
                ),
                title="Errands",
                item_id="errands",
            ),
            # Lodging Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        # Hotel
                        html.Div([
                            html.H6("Hotel", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "hotel-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(hotel_layers)
                            ])
                        ]),
                    ]
                ),
                title="Lodging",
                item_id="lodging",
            ),
            # Shop Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        # Retail (Consumer Goods)
                        html.Div([
                            html.H6("Consumer Goods", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "consumergoods-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(consumergoods_layers)
                            ])
                        ]),
                        # Retail (Durable Goods)
                        html.Div([
                            html.H6("Durable Goods", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "durablegoods-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(durablegoods_layers)
                            ])
                        ]),
                        # Retail (Grocery)
                        html.Div([
                            html.H6("Grocery", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "grocery-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(grocery_layers)
                            ])
                        ]),
                    ]
                ),
                title="Shop",
                item_id="shop",
            ),
            # Recreation Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        # Cultural
                        html.Div([
                            html.H6("Cultural", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "cultural-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(cultural_layers)
                            ])
                        ]),
                        # Entertainment
                        html.Div([
                            html.H6("Entertainment", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "entertainment-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(entertainment_layers)
                            ])
                        ]),
                        # Leisure & Wellness
                        html.Div([
                            html.H6("Leisure & Wellness", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "leisurewellness-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(leisurewellness_layers)
                            ])
                        ]),
                    ]
                ),
                title="Recreation",
                item_id="recreation",
            ),
            # Transport Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        # Train
                        html.Div([
                            html.H6("Train", style={"marginTop": "10px", "marginBottom": "5px"}),
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
                        # Bus
                        html.Div([
                            html.H6("Bus", style={"marginTop": "10px", "marginBottom": "5px"}),
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
                        # Bike
                        html.Div([
                            html.H6("Bike", style={"marginTop": "10px", "marginBottom": "5px"}),
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
            # Errands Section
            dbc.AccordionItem(
                dmc.MantineProvider(
                    children=[
                        # Religious
                        html.Div([
                            html.H6("Religious", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "religious-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(religious_layers)
                            ])
                        ]),
                    ]
                ),
                title="Others",
                item_id="others",
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
                    id="geojson-layer",
                    data=geojson,  # Replace with your actual endpoint
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

# Update the callback to display the hovered feature's information, including CUSEC
@callback(Output("info", "children"), Input("geojson-layer", "hoverData"))
def info_hover(feature):
    return get_info(feature)

@app.callback(
    Output('geojson-layer', 'data'),
    [Input({"type": "educational-item", "index": ALL}, "checked")]  # Listen for changes in the checked state of the color checkboxes
)
def update_color(checked_values):
    # Update the selected colors based on checkbox input (checked state)
    selected_colors = []

    # Iterate over the checked values to gather the selected colors
    for idx, checked in enumerate(checked_values):
        if checked:  # If the checkbox is checked
            selected_colors.append(educational_layers[idx]["value"])  # Get the value of the selected color

    # Update the GeoJSON based on the selected colors
    for feature in geojson['features']:
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

    return geojson  # Return the updated GeoJSON data

if __name__ == "__main__":
    app.run_server(debug=True)
