import dash
from dash import html, Input, Output, ALL, callback, ctx, _dash_renderer
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_leaflet as dl
from dash import dcc
from dash_extensions.javascript import assign
import json

visual_style = assign("""
    function(feature) {
        return {
            color: '#3182bd',
            weight: 2,
            opacity: 0.8,
            fillColor: feature.properties.color || '#6baed6',
            fillOpacity: 0.4
        };
    }
""")

# Inline JavaScript to fetch CSV based on selection
load_data_script = assign("""
    function(selectedOption) {
        const urlMap = {
            "Hospitals": '/assets/hospitals.csv',
            "Schools": '/assets/schools.csv',
            "Libraries": '/assets/libraries.csv'
        };
        
        const url = urlMap[selectedOption];
        if (url) {
            fetch(url)
                .then(response => response.text())
                .then(data => {
                    const features = parseCSVToGeoJSON(data);
                    const geojsonData = {
                        type: "FeatureCollection",
                        features: features
                    };
                    return geojsonData;
                });
        }
        
        // Helper function to parse CSV into GeoJSON format
        function parseCSVToGeoJSON(csvData) {
            const rows = csvData.split("\\n");
            const features = rows.slice(1).map(row => {
                const cols = row.split(",");
                return {
                    type: "Feature",
                    geometry: {
                        type: "Point",
                        coordinates: [parseFloat(cols[1]), parseFloat(cols[2])]  // lon, lat
                    },
                    properties: {
                        Referencia: cols[0],
                        nearest_poi: cols[6],
                        nearest_node: cols[3],
                        time_to_nearest_poi: cols[4],
                        distance_to_nearest_poi: cols[8]
                    }
                };
            });
            return features;
        }
    }
""")

# Dash app
_dash_renderer._set_react_version("18.2.0")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

# Layout
app.layout = dmc.MantineProvider(  # Wrap the layout with MantineProvider
    children=html.Div(
        [
            dl.Map(
                [
                    dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', maxZoom=20),
                    dl.GeoJSON(id="geojson", options=dict(style=visual_style)),
                    dl.LayerGroup(id="map-points"),
                ],
                center=[43.3, -2.0],
                zoom=11,
                style={"height": "100vh", "width": "100%"},
            ),
            dmc.Select(
                id="poi-selector",
                label="Select POI category",
                data=["Hospitals", "Schools", "Libraries"],
                value="Hospitals"
            ),
            # Store to pass the selected POI category
            dcc.Store(id="store-selected-option")
        ]
    )
)

# Callback to update store with the selected value
@app.callback(
    Output("store-selected-option", "data"),
    Input("poi-selector", "value")
)
def update_store(selected_option):
    return {"selected_option": selected_option}

# Callback to update the GeoJSON layer based on selection
@app.callback(
    Output("geojson", "data"),
    Input("store-selected-option", "data")
)
def update_map(selected_option_data):
    selected_option = selected_option_data["selected_option"]
    return load_data_script(selected_option)  # Call the javascript function

if __name__ == "__main__":
    app.run_server(debug=True)

