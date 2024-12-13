import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html
from dash.dependencies import Input, Output
from dash_extensions.javascript import arrow_function, assign

def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + [html.P("Hover over a state")]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]

classes = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']
style = dict(weight=2, opacity=1, color='black', fillColor='white', dashArray='3', fillOpacity=0.5)

# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""
function(feature, context){
    const {classes, colorscale, style, colorProp} = context.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value that determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")

# Non-interactive layer with default color styling
non_interactive_layer = dl.GeoJSON(
    url="/assets/aggregated_buildings_multipolygons_sections.geojson",  # url to geojson file
    style=style_handle,  # how to style each polygon
    zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="density"),
    id="non_interactive_geojson"
)

# Interactive layer with hover effect
interactive_style = arrow_function(dict(weight=5, color='#666', dashArray=''))  # style applied on hover
interactive_layer = dl.GeoJSON(
    url="/assets/aggregated_buildings_multipolygons_sections.geojson",  # url to geojson file
    style={'fillOpacity': 0},  # Transparent fill color
    hoverStyle=interactive_style,  # style applied on hover
    id="interactive_geojson"
)

# Create info control.
info = html.Div(
    children=get_info(), id="info", className="info",
    style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"}
)

# Initialize the Dash app
app = dash.Dash(prevent_initial_callbacks=True)

# Layout of the app
app.layout = html.Div([ 
    dl.Map(children=[  
        dl.TileLayer(),
        non_interactive_layer,  # Non-interactive layer showing colors
        interactive_layer,  # Interactive layer for hovering
        colorbar, 
        info
    ], style={'height': '99vh', 'width': '99vw', 'margin': '0', 'overflow': 'hidden'}, center=[56, 10], zoom=6)
])

# Callback to update the info based on the hovered feature
@app.callback(Output("info", "children"), Input("interactive_geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)

if __name__ == '__main__':
    app.run_server(debug=False)




