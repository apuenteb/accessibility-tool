import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function, assign

def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + [html.P("Hover over a state")]
    
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


classes = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")

# Create geojson with both style and hoverStyle
geojson = dl.GeoJSON(
    url="/assets/sections_gipuzkoa.geojson",  # url to geojson file
    style=style_handle,  # how to style each polygon
    zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
    hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="density"),
    onEachFeature=arrow_function("""
        function(feature, layer) {
            layer.on('mouseover', function() {
                layer.setStyle({weight: 5, color: '#666', dashArray: ''}); // apply hover style
            });
            layer.on('mouseout', function() {
                layer.setStyle({weight: 2, color: 'white', dashArray: '3'}); // revert to normal style
            });
        }
    """),
    id="geojson"
)

# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"})

# Create app.
app = Dash(prevent_initial_callbacks=True)
app.layout = dl.Map(children=[dl.TileLayer(), geojson, colorbar, info],
                    style={'height': '100vh'}, center=[56, 10], zoom=6)

# Update the callback to display the hovered feature's information, including CUSEC
@app.callback(Output("info", "children"), Input("geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)

if __name__ == '__main__':
    app.run_server()
