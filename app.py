import dash
from dash import html
from flask import send_file

# Dash app
app = dash.Dash(__name__)

# Serve the HTML template directly
@app.server.route('/leaflet_map')
def serve_leaflet_map():
    return send_file('leaflet_map.html')

# Serve the GeoJSON file
@app.server.route('/geojson')
def serve_geojson():
    return send_file('aggregated_buildings_multipolygons_sections.geojson')

# Dash layout
app.layout = html.Div(
    children=[
        html.Iframe(
            src="/leaflet_map",
            style={"height": "100vh", "width": "100vw", "border": "none"},
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)


