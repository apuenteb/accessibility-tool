import dash_bootstrap_components as dbc 
import dash
import dash_mantine_components as dmc
from dash import html, _dash_renderer, Input, Output, ALL, callback, ctx

_dash_renderer._set_react_version("18.2.0")

################################################## SETUP ################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
server = app.server

######################################### INITIALIZATION OF VARIABLES ################################################################
fb_values = [
    {"id": "catering", "label": "Catering", "checked": False},
    {"id": "bars", "label": "Bars", "checked": False},
    {"id": "restaurants", "label": "Restaurants", "checked": False},
    {"id": "cafes", "label": "Cafes", "checked": False},
]

################################################## LAYOUT ################################################################
app.layout = html.Div([
    dbc.Accordion(
        [
            dbc.AccordionItem(
                dmc.MantineProvider(
                            children=html.Div([
                            dmc.Checkbox(
                                id="all-eatery",
                                label="F&B Eatery",
                                checked=False,
                                indeterminate=False
                            ),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "eatery-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "33px"}
                                )
                                for i, item in enumerate(fb_values)
                            ])
                        ])
                ),
                title="Eat",
                item_id="eat",
            ),
            dbc.AccordionItem(
                "This is the content of the second section",
                title="Errands",
                item_id="errands",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Lodging",
                item_id="lodging",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Shop",
                item_id="shop",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Recreation",
                item_id="recreation",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Transport",
                item_id="transport",
            ),
            dbc.AccordionItem(
                "This is the content of the third section",
                title="Others",
                item_id="others",
            ),
        ],
        id="accordion",
        active_item="item-1",
    ),
    html.Div(id="accordion-contents", className="mt-3"),
])

############################################### CALLBACKS ################################################################

@callback(
    Output("all-eatery", "checked"),
    Output("all-eatery", "indeterminate"),
    Output({"type": "eatery-item", "index": ALL}, "checked"),
    Input("all-eatery", "checked"),
    Input({"type": "eatery-item", "index": ALL}, "checked"),
    prevent_initial_callback=True
)
def update_main_checkbox(all_checked, checked_states):
    # handle "all" checkbox"
    if ctx.triggered_id == 'all-eatery':
        checked_states = [all_checked] * len(checked_states)

    # handled individual check boxes
    all_checked_states = all(checked_states)
    indeterminate = any(checked_states) and not all_checked_states
    return all_checked_states, indeterminate, checked_states

################################################## RUN ################################################################

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
