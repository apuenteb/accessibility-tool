import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Sample data
df = px.data.gapminder().query("year==2007")

app.layout = html.Div([
    dcc.Dropdown(
        id='color-dropdown',
        options=[
            {'label': 'Black', 'value': 'black'},
            {'label': 'Red', 'value': 'red'},
            {'label': 'Blue', 'value': 'blue'}
        ],
        value='black'
    ),
    dcc.Graph(id='map-graph')
])

@app.callback(
    Output('map-graph', 'figure'),
    Input('color-dropdown', 'value')
)
def update_map(color):
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="lifeExp",
        projection="natural earth"
    )

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor=color,
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue"
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)