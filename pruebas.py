import dash
from dash import html, Output, Input
from pathlib import Path
from flask import send_file

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Paths for HTML files
base_html_path = Path("assets/base_map.html")
generated_html_path = Path("assets/generated_map.html")
leaflet_html_path = Path("assets/leaflet_map.html")
leaflet_html = leaflet_html_path.read_text()

# Define the layout with buttons for interaction and an iframe for the map
app.layout = html.Div([
    html.H1("ACCESSIBILITY TOOL"),
    html.Button("Accessibility Data", id="button-access"),
    html.Button("Socioeconomic Data", id="button-socio"),
    html.Iframe(id="leaflet-map", style={"width": "100%", "height": "90vh"}),
])

@app.callback(
    Output("leaflet-map", "srcDoc"),
    [Input("button-access", "n_clicks"),
     Input("button-socio", "n_clicks")]
)
def update_map(button1_clicks, button2_clicks):
    # Load the base HTML (the static map layout)
    base_html = base_html_path.read_text()

    # Determine which button was clicked and select appropriate GeoJSON and styles
    if button1_clicks is not None and button1_clicks > 0:
        geojson_path = 'data/aggregated_buildings_multipolygons_sections.geojson'
        style = """
        const highlightStyle = { color: '#ff0000', weight: 3, opacity: 1 };
        const defaultStyle = { color: '#3182bd', weight: 2, opacity: 0.8 };
        """
        button2_clicks = None  # Reset the other button
    elif button2_clicks is not None and button2_clicks > 0:
        geojson_path = 'data/geojson_file2.geojson'
        style = """
        const highlightStyle = { color: '#00ff00', weight: 3, opacity: 1 };
        const defaultStyle = { color: '#3182bd', weight: 2, opacity: 0.8 };
        """
        button1_clicks = None  # Reset the other button
    else:
        return leaflet_html  # Return base map if no button is clicked

    # Generate the dynamic JavaScript code to add GeoJSON
    dynamic_js = f"""<script>
  // Check if map is already defined to avoid redeclaring it
  if (typeof map === 'undefined') {{
      const map = L.map('map').setView([43.3, -2.0], 11);

    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
      maxZoom: 19,
    }}).addTo(map);
  }}

  // Define styles for GeoJSON
  const highlightStyle = {{ color: '#ff0000', weight: 3, opacity: 1 }};
  const defaultStyle = {{ color: '#3182bd', weight: 2, opacity: 0.8 }};

  // Fetch GeoJSON data based on button clicked
  fetch('/data/geojson_file1.geojson')
    .then(response => response.json())
    .then(geojsonData => {{
      const geojsonLayer = L.geoJson(geojsonData, {{
        style: defaultStyle,
        onEachFeature: (feature, layer) => {{
          layer.on('mouseover', () => {{
            layer.setStyle(highlightStyle);
          }});
          layer.on('mouseout', () => {{
            geojsonLayer.resetStyle(layer);
          }});
          layer.bindTooltip(
            `<strong>${{feature.properties['CUSEC']}}</strong><br>Municipio: ${{feature.properties['Municipio']}}`,
            {{ permanent: false, direction: 'top' }}
          );
        }},
      }}).addTo(map);
    }})
    .catch(error => console.error('Error loading GeoJSON:', error));
</script>
"""
    # Combine the base HTML with the dynamic JavaScript
    full_html = base_html.replace("</body>", f"{dynamic_js}</body>")

    # Save the generated HTML (optional, for future reference)
    generated_html_path.write_text(full_html)

    return full_html  # Return the updated HTML

# Route to serve GeoJSON files
@app.server.route('/data/<filename>')
def serve_geojson(filename):
    return send_file(f'data/{filename}')

if __name__ == "__main__":
    app.run_server(debug=False)

