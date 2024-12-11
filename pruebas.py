import dash
from dash import html
from flask import send_file
import dash_mantine_components as dmc

# Set the React version for Dash Mantine Components
from dash import _dash_renderer
_dash_renderer._set_react_version("18.2.0")

# Dash app setup
app = dash.Dash(external_stylesheets=dmc.styles.ALL)
server = app.server

# Flask route to serve the Leaflet map
@app.server.route('/assets/prueba_map')
def serve_leaflet_map():
    return send_file('assets/prueba_map.html')

# Layout with sidebar over the map
app.layout = html.Div(
    style={"position": "relative", "height": "100vh"},
    children=[
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

        # Sidebar content
        html.Div(
            style={
                "position": "absolute",
                "top": "10px",
                "left": "10px",
                "width": "350px",
                "backgroundColor": "white",
                "padding": "10px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                "zIndex": 2,  # Ensure it's above the map
            },
            children=[
                dmc.MantineProvider(
                    [
                        dmc.Title("Select the Points of Interest", order=3),
                        dmc.ScrollArea(
                            h=250,
                            w=350,
                            children=dmc.Stack(
                                [
                                    dmc.Checkbox(id="farmacias", checked=False, label="Pharmacies"),
                                    dmc.Checkbox(id="bibliotecas-publicas", checked=False, label="Public libraries"),
                                    dmc.Checkbox(id="colegios", checked=False, label="Schools"),
                                    dmc.Checkbox(id="supermercados", checked=False, label="Supermarkets"),
                                    dmc.Checkbox(id="instalaciones-deportivas", checked=False, label="Sports facilities"),
                                    dmc.Checkbox(id="restaurantes", checked=False, label="Restaurants"),
                                    dmc.Checkbox(id="gym", checked=False, label="Gyms"),
                                    dmc.Checkbox(id="paradas-pt", checked=False, label="Public transport stops"),
                                ]
                            ),
                        ),
                    ]
                )
            ],
        ),
    ],
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
