from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd

# Load your dataset
df = gpd.read_file("data/sections_gipuzkoa_demographic_women.geojson")  
geojson = gpd.read_file("data/sections_gipuzkoa.geojson")  

# Initialize Dash app
app = Dash(__name__)

# Create app layout
app.layout = html.Div(
    [
        html.H4("Female Population in Gipuzkoa"),
        html.P("Select an age group:"),
        dcc.RadioItems(
            id="age_group",
            options=[
                {"label": "Total", "value": "Total"},
                {"label": "0-19 years", "value": "0-19 años"},
                {"label": "20-34 years", "value": "20-34 años"},
                {"label": "35-49 years", "value": "35-49 años"},
                {"label": "50-64 years", "value": "50-64 años"},
                {"label": "65-84 years", "value": "65-84 años"},
                {"label": "85+ years", "value": "85+ años"},
            ],
            value="Total",
            inline=True,
        ),
        dcc.Graph(
            id="graph",
            style={"height": "1100px", "width": "100%"},  # Adjust height and width here
        ),
    ]
)

# Define callback
@app.callback(
    Output("graph", "figure"),
    Input("age_group", "value"),
)
def display_choropleth(age_group):
    # Create the choropleth map with a custom color scale
    fig = px.choropleth(
        df,
        geojson=geojson,
        color=age_group,
        locations="CUSEC",
        featureidkey="properties.CUSEC",  # Adjust if necessary
        projection="mercator",
        color_continuous_scale="Blues",  # Replace with your chosen scale
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# Run app
if __name__ == "__main__":
    app.run_server(debug=False)