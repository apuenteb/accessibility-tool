from dash import html
import dash_leaflet as dl
from dash import Dash
from dash.dependencies import Output, Input
from dash_extensions.javascript import assign
import geopandas as gpd
import json
from dash import dash_table

# JavaScript function for styling
style_handle = assign("""function(feature, context){
    const match = context.props.hideout && context.props.hideout.properties.name === feature.properties.name;
    if(match) return {weight: 5, color: '#666', dashArray: ''};
    return {color: '#3388ff', weight: 2, fillOpacity: 0.6};  // Default styling
}""")

#https://gist.github.com/incubated-geek-cc/5da3adbb2a1602abd8cf18d91016d451?short_path=2de7e44
us_states_gdf = gpd.read_file("./assets/states.geojson")
us_states_geojson = json.loads(us_states_gdf.to_json())

# Create example app
app = Dash(__name__)
app.layout = html.Div([
    dl.Map(center=[39, -98], zoom=4, children=[
        dl.TileLayer(),
        dl.GeoJSON(
            id="states",
            data=us_states_geojson,
        )
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
    html.Div(id='state-container', children=[]),  #
    dash_table.DataTable(id='state-table', columns=[{"name": i, "id": i} for i in ["state"]], data=[])
])

# Update the feature saved on the hideout prop on click
app.clientside_callback(
    "function(feature){return feature}", 
    Output("states", "hideout"), 
    [Input("states", "click_feature")]
)

if __name__ == '__main__':
    app.run_server()