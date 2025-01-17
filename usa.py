import random, json
import dash
from dash import dcc, html, Dash, callback, Output, Input, State
import dash_leaflet as dl
import geopandas as gpd
from dash import dash_table
from dash_extensions.javascript import assign

#https://gist.github.com/incubated-geek-cc/5da3adbb2a1602abd8cf18d91016d451?short_path=2de7e44
us_states_gdf = gpd.read_file("/assets/states.geojson")
us_states_geojson = json.loads(us_states_gdf.to_json())
# Color the feature saved in the hideout prop in a particular way (grey).
style_handle = assign("""function(feature, context){
    const match = context.props.hideout &&  context.props.hideout.properties.name === feature.properties.name;
    if(match) return {color:'#126'};
}""")

app = Dash(__name__)
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(url="http://tile.stamen.com/toner-lite/{z}/{x}/{y}.png"),
        dl.GeoJSON(data=us_states_geojson, id="state-layer",
                   options=dict(style=style_handle), hideout=dict(click_feature=None))],
        style={'width': '100%', 'height': '250px'},
        id="map",
        center=[39.8283, -98.5795],
    ),
    html.Div(id='state-container', children=[]),  #
    dash_table.DataTable(id='state-table', columns=[{"name": i, "id": i} for i in ["state"]], data=[])
])
# Update the feature saved on the hideout prop on click.
app.clientside_callback("function(feature){return feature}",
                        Output("state-layer", "hideout"),
                        [Input("state-layer", "click_feature")])

app.clientside_callback(
    """
    function(clickFeature, currentData) {
        if(!clickFeature){
            return window.dash_clientside.no_update
        }

        const state = clickFeature.properties.NAME
        const currentStates = currentData.map(item => item.state)

        let newData = []
        if(!currentStates.includes(state)){
            newData = [...currentData, {"state": state}]
        }else{
            newData = currentData
        }

        const stateText = `Clicked: ${state}`
        return [newData, stateText]
    }
    """,
    Output("state-table", "data"),
    Output("state-container", "children"),
    Input("state-layer", "click_feature"),
    State("state-table", "data"),
)

if __name__ == '__main__':
    app.run_server(debug=True)