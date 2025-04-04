import dash
from dash import html, Input, Output, ALL, callback, ctx, _dash_renderer, dcc, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_leaflet as dl
from dash_extensions.javascript import assign
import json
import dash_leaflet.express as dlx
import pandas as pd
from multiprocessing import freeze_support
from flask import Flask
from flask_socketio import SocketIO, emit

#Link to PM: https://cityscope.media.mit.edu/CS_cityscopeJS_projection_mapping/?cityscope=nombre_de_la_mesa

from cityio import CityIo

message = ''

def main():
    cityio = CityIo(is_local=True)
    #cityio = CityIo(is_local=False)
    cityio.start()

    # python -m venv venv
    # On Windows: venv\Scripts\activate
    # pip freeze > requirements.txt
    # pip install -r requirements.txt

    # load csv into pandas dataframe
    TIME_DATA = pd.read_csv('./assets/csv_files/time_data.csv', dtype={"Referencia": str})
    buildings_df = pd.read_csv("./assets/csv_files/buildings_by_section.csv", dtype=str)  # lee todas las columnas como str)
    buildings_df['Referencia'] = buildings_df['Referencia'].astype(str)
    print(buildings_df.head())

    server = Flask(__name__)
    app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
    socketio = SocketIO(server)

    def get_info(feature=None, selected_pois=None, transport_mode=None, time_data=TIME_DATA):
        # Default header when no feature is hovered
        header = [html.H4("Hover over a block for details")]
        if not feature:
            return header + [html.P("")]

        if transport_mode == "walk":
            transport_msg = html.B("Walking time to:")
        elif transport_mode == "bike":
            transport_msg = html.B("Biking time to:")
        elif transport_mode == "pt":
            transport_msg = html.B("Public transit time to:")
        elif transport_mode == "car":
            transport_msg = html.B("Driving time to:")

        # Extract properties from the feature
        ref = feature["properties"].get("Referencia", None)

        # Initialize poi_times as an empty list to avoid UnboundLocalError
        poi_times = []

        # Ensure `ref` is a string for comparison
        if time_data is not None and ref:
            ref = str(ref).strip()  # Convert and clean `ref`

            # Filter the DataFrame for the matching `Referencia`
            row = time_data[time_data["Referencia"] == ref]

            # Check if row is empty
            if not row.empty:
                # For each selected POI, get the corresponding time based on the transport mode
                for column in selected_pois:
                    column_with_mode = f"{column}_{transport_mode}"

                    # Check if the column exists before trying to access it
                    if column_with_mode in row.columns:
                        time = row[column_with_mode].iloc[0]  # Get the time for this POI and mode of transport
                    else:
                        time = "N/A"

                    poi_label = layer_labels.get(column, column.replace("_", " ").capitalize())

                    # Add the time info to the list
                    poi_times.append(html.P([html.B(poi_label), f": {time} minutes"], style={"margin": "0", "padding": "0"}))
            else:
                # Add a message when no data is found
                poi_times.append(html.P("No data available for this feature", style={"margin": "0", "padding": "0"}))

        # Default ref value if it's None
        ref = ref if ref else "N/A"

        # Build the HTML output
        return [
            transport_msg, html.Br(),
            html.Div(
                [html.Div(poi_time, style={"margin": "0", "padding": "0"}) for poi_time in poi_times],
                style={"display": "flex", "flex-direction": "column", "gap": "1px"}
            ),
            html.Div(f"Referencia: {ref}", style={"margin": "0", "padding": "0"}),
        ]

    # Arduino websocket functions
    @socketio.on('connect', namespace='/test')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect', namespace='/test')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('message', namespace='/test')
    def handle_message(mess):
        global message
        message = mess
        print(f'Received message: {message}')
        socketio.emit('update', '', namespace='/test')


    @app.callback(
        [Output('donostia-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'donostia':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    @app.callback(
        [Output('debab-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'debab':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    @app.callback(
        [Output('debag-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'debag':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    @app.callback(
        [Output('bidasoa-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'bidasoa':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    @app.callback(
        [Output('goierri-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'goierri':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    @app.callback(
        [Output('urolak-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'urolak':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    @app.callback(
        [Output('tolosa-button', 'n_clicks')],
        [Input('interval', 'n_intervals')]
    )
    def click_button(n_intervals):
        global message
        if len(message) > 0 and message == 'tolosa':
            print('sending click request')
            message = ''
            return [1]
        else:
            return [0]  # return current state when message is empty

    #################################################################################

    # Create info control.
    info = html.Div(
        children=get_info(),
        id="info",
        className="info",
        style={
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "zIndex": "1000",
            "backgroundColor": "rgba(255, 255, 255, 1)",  # Semi-transparent background
            "padding": "10px",  # Optional: Add some padding for better readability
            "borderRadius": "5px",  # Optional: Rounded corners
            "border": "1px solid #ccc"
        }
    )

    # styling of the polygons (default & when hovered)
    visual_style = assign("""
        function(feature) {
            const selectedColor = feature.properties.selectedColor || '#6baed6'; // Default color (blue)
            const selectedOpacity = feature.properties.selectedOpacity || 0.4; // Default color (blue)
            return {
                color: '#3182bd',
                weight: 0.5,
                opacity: 0.8,
                fillColor: selectedColor,
                fillOpacity: selectedOpacity
            };
        }
    """)

    on_each_feature = assign("""
        function(feature, layer) {
            // Mouseover event
            layer.on('mouseover', function() {
                if (!layer.options._originalStyle) {
                    // Save the original style if not already saved
                    layer.options._originalStyle = {
                        color: layer.options.color,
                        weight: layer.options.weight,
                        opacity: layer.options.opacity,
                        fillColor: layer.options.fillColor,
                        fillOpacity: layer.options.fillOpacity,
                    };
                }
                // Apply highlight style only to the hovered feature
                layer.setStyle({
                    color: '#2b5775',
                    weight: 3,
                    opacity: 1,
                    fillOpacity: 0.7
                });
            });

            // Mouseout event
            layer.on('mouseout', function() {
                if (layer.options._originalStyle) {
                    // Reset the style of the hovered feature
                    layer.setStyle(layer.options._originalStyle);
                }
            });
        }
    """)


    # Dash app (initialize like here always, if not the dmc components don't work, we need to make sure the React version is 18.2.0)
    # React 18 Issue: Dash Mantine Components is based on REACT 18. You must set the env variable REACT_VERSION=18.2.0 before starting up the app.
    # https://www.dash-mantine-components.com/getting-started#:~:text=React%2018%20Issue,up%20the%20app.
    _dash_renderer._set_react_version("18.2.0")
    #app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
    #server = app.server
    #server = Flask(__name__)
    #app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL])
    #socketio = SocketIO(server)

    # Custom icon (using local assets)
    custom_icon = dict(
        iconUrl='/assets/icons/icon_blue1.png',  # Local icon
        iconSize=[10, 10], # size in px
        iconAnchor=[5, 5], # point of the icon which will correspond to marker's location, as we have a circle, the half of the size
    )

    # Load geojson polygons
    with open("assets/geojsons/buildings_by_section_small.geojson", "r") as f:
        geojson = json.load(f)

    # Load geojson polygons
    with open("assets/geojsons/sections_colores.geojson", "r") as f:
        projected_geojson = json.load(f)
    cityio.send_geojson(projected_geojson)

    ###### EAT GEOJSON
    with open("assets/geojsons/restaurantes.geojson", "r", encoding='utf-8') as f:
        restaurantes_geojson = json.load(f)

    with open("assets/geojsons/cafe.geojson", "r", encoding='utf-8') as f:
        cafe_geojson = json.load(f)

    with open("assets/geojsons/bares.geojson", "r", encoding='utf-8') as f:
        bares_geojson = json.load(f)

    # Dictionaries by POI categories
    eat_layers = [
        {"label": "Restaurants", "value":"restaurantes", "geojson":restaurantes_geojson,"checked": False},
        {"label": "Cafes & bakeries",  "value":"cafe", "geojson":cafe_geojson,"checked": False},
        {"label": "Bars", "value":"bares", "geojson":bares_geojson,"checked": False},
    ]

    #### EDUCATION GEOJSON
    with open("assets/geojsons/infantil.geojson", "r", encoding='utf-8') as f:
        infantil_geojson = json.load(f)

    with open("assets/geojsons/primaria.geojson", "r", encoding='utf-8') as f:
        primaria_geojson = json.load(f)

    with open("assets/geojsons/secundaria.geojson", "r", encoding='utf-8') as f:
        secundaria_geojson = json.load(f)
    
    with open("assets/geojsons/universidad.geojson", "r", encoding='utf-8') as f:
        universidad_geojson = json.load(f)
    
    with open("assets/geojsons/fp.geojson", "r", encoding='utf-8') as f:
        fp_geojson = json.load(f)
    
    with open("assets/geojsons/educ_otros.geojson", "r", encoding='utf-8') as f:
        educ_otros_geojson = json.load(f)    

    with open("assets/geojsons/educ_polideportiva_recreativa.geojson", "r", encoding='utf-8') as f:
        educ_polideportiva_recreativa_geojson = json.load(f)

    school_layers = [
        {"label": "Kindergarten",  "value":"infantil", "geojson":infantil_geojson,"checked": False},
        {"label": "Elementary School",  "value":"primaria", "geojson":primaria_geojson,"checked": False},
        {"label": "High School", "value":"secundaria", "geojson":secundaria_geojson,"checked": False},
        {"label": "Universities",  "value":"universidad", "geojson":universidad_geojson,"checked": False},
        {"label": "Professional Education", "value":"fp", "geojson":fp_geojson,"checked": False},
        {"label": "Other Education Centers", "value":"educ_otros", "geojson":educ_otros_geojson,"checked": False},
        {"label": "Sports and Recreation Instruction", "value":"educ_polideportiva_recreativa", "geojson":educ_polideportiva_recreativa_geojson,"checked": False},
    ]

    #### HEALTHCARE GEOJSON
    with open("assets/geojsons/centros_salud.geojson", "r", encoding='utf-8') as f:
        centros_salud_geojson = json.load(f)
    
    with open("assets/geojsons/hospital.geojson", "r", encoding='utf-8') as f:
        hospital_geojson = json.load(f)
    
    with open("assets/geojsons/nursing.geojson", "r", encoding='utf-8') as f:
        nursing_geojson = json.load(f)
    
    with open("assets/geojsons/dentista.geojson", "r", encoding='utf-8') as f:
        dentista_geojson = json.load(f)    

    with open("assets/geojsons/other_healthcare.geojson", "r", encoding='utf-8') as f:
        other_healthcare_geojson = json.load(f)

    healthcare_layers = [
        {"label": "Clinics & local healthcare centers", "value": "centros_salud", "geojson": centros_salud_geojson,"checked": False},
        {"label": "Hospitals", "value":"hospital","geojson":hospital_geojson,"checked": False},
        {"label": "Nursing & Residential Care", "value":"nursing","geojson":nursing_geojson,"checked": False},
        {"label": "Dentists", "value":"dentista","geojson":dentista_geojson,"checked": False},
        {"label": "Other Healthcare Services", "value":"other_healthcare","geojson":other_healthcare_geojson,"checked": False},
    ]

    #### LEISURE & WELLNESS GEOJSON
    with open("assets/geojsons/estetica.geojson", "r", encoding='utf-8') as f:
        estetica_geojson = json.load(f)

    leisure_layers = [
        {"label": "Personal Grooming & Wellness", "value":"estetica","geojson":estetica_geojson,"checked": False},
    ]

    #### PROFESSIONAL SERVICES GEOJSON
    with open("assets/geojsons/administrative.geojson", "r", encoding='utf-8') as f:
        administrative_geojson = json.load(f)
    
    with open("assets/geojsons/finance.geojson", "r", encoding='utf-8') as f:
        finance_geojson = json.load(f)
    
    with open("assets/geojsons/insurance.geojson", "r", encoding='utf-8') as f:
        insurance_geojson = json.load(f)
    
    with open("assets/geojsons/professional_services.geojson", "r", encoding='utf-8') as f:
        professional_services_geojson = json.load(f)
    
    with open("assets/geojsons/real_estate.geojson", "r", encoding='utf-8') as f:
        real_estate_geojson = json.load(f)
    
    with open("assets/geojsons/agencia_viajes.geojson", "r", encoding='utf-8') as f:
        agencia_viajes_geojson = json.load(f)

    professional_layers = [
        {"label": "Administrative and Support Services", "value":"administrative","geojson":administrative_geojson,"checked": False},
        {"label": "Finance", "value":"finance","geojson":finance_geojson,"checked": False},
        {"label": "Insurance Agency", "value":"insurance","geojson":insurance_geojson,"checked": False},
        {"label": "Professional Services", "value":"professional_services","geojson":professional_services_geojson,"checked": False},
        {"label": "Real Estate", "value":"real_estate","geojson":real_estate_geojson,"checked": False},
        {"label": "Travel Agency", "value":"agencia_viajes","geojson":agencia_viajes_geojson,"checked": False},
    ]

    #### PHARMACY GEOJSON
    with open("assets/geojsons/farmacia.geojson", "r", encoding='utf-8') as f:
        farmacia_geojson = json.load(f)

    pharmacy_layers = [
        {"label": "Pharmacy", "value": "farmacia", "geojson": farmacia_geojson,"checked": False},
    ]

    #### SERVICE GEOJSON
    with open("assets/geojsons/car_rental.geojson", "r", encoding='utf-8') as f:
        car_rental_geojson = json.load(f)
    
    with open("assets/geojsons/car_repair.geojson", "r", encoding='utf-8') as f:
        car_repair_geojson = json.load(f)
    
    with open("assets/geojsons/funebre.geojson", "r", encoding='utf-8') as f:
        funebre_geojson = json.load(f)
    
    with open("assets/geojsons/gasolinera.geojson", "r", encoding='utf-8') as f:
        gasolinera_geojson = json.load(f)
    
    with open("assets/geojsons/lavanderia_tintoreria.geojson", "r", encoding='utf-8') as f:
        lavanderia_tintoreria_geojson = json.load(f)
    
    with open("assets/geojsons/cerrajero.geojson", "r", encoding='utf-8') as f:
        cerrajero_geojson = json.load(f)
    
    with open("assets/geojsons/mudanzas.geojson", "r", encoding='utf-8') as f:
        mudanzas_geojson = json.load(f)
    
    with open("assets/geojsons/parking.geojson", "r", encoding='utf-8') as f:
        parking_geojson = json.load(f)
    
    with open("assets/geojsons/post_office.geojson", "r", encoding='utf-8') as f:
        post_office_geojson = json.load(f)
    
    with open("assets/geojsons/veterinario.geojson", "r", encoding='utf-8') as f:
        veterinario_geojson = json.load(f)

    with open("assets/geojsons/gestion_residuos.geojson", "r", encoding='utf-8') as f:
        gestion_residuos_geojson = json.load(f)

    service_layers = [
        {"label": "Car Rental", "value": "car_rental", "geojson": car_rental_geojson,"checked": False},
        {"label": "Car Repair", "value": "car_repair", "geojson": car_repair_geojson,"checked": False},
        {"label": "Death Care Services", "value": "funebre", "geojson": funebre_geojson,"checked": False},
        {"label": "Fuel Station", "value": "gasolinera", "geojson": gasolinera_geojson,"checked": False},
        {"label": "Laundry", "value": "lavanderia_tintoreria", "geojson": lavanderia_tintoreria_geojson,"checked": False},
        {"label": "Locksmith Errands", "value": "cerrajero", "geojson": cerrajero_geojson,"checked": False},
        {"label": "Moving Company", "value": "mudanzas", "geojson": mudanzas_geojson,"checked": False},
        {"label": "Parking", "value": "parking", "geojson": parking_geojson,"checked": False},
        {"label": "Post Office", "value": "post_office", "geojson": post_office_geojson,"checked": False},
        {"label": "Veterinary Services", "value": "veterinario", "geojson": veterinario_geojson,"checked": False},
        {"label": "Waste Management", "value": "gestion_residuos", "geojson": gestion_residuos_geojson,"checked": False},
    ]

    #### HOTEL GEOJSON
    with open("assets/geojsons/hotel.geojson", "r", encoding='utf-8') as f:
        hotel_geojson = json.load(f)

    hotel_layers = [
        {"label": "Hotel and Lodging", "value": "hotel", "geojson": hotel_geojson,"checked": False},
    ]

    #### CONSUMER GOODS GEOJSONS
    with open("assets/geojsons/libreria.geojson", "r", encoding='utf-8') as f:
        libreria_geojson = json.load(f)
    
    with open("assets/geojsons/tiendas_ropa.geojson", "r", encoding='utf-8') as f:
        tiendas_ropa_geojson = json.load(f)
    
    with open("assets/geojsons/cosmeticos.geojson", "r", encoding='utf-8') as f:
        cosmeticos_geojson = json.load(f)
    
    with open("assets/geojsons/bazar.geojson", "r", encoding='utf-8') as f:
        bazar_geojson = json.load(f)
    
    with open("assets/geojsons/floristeria.geojson", "r", encoding='utf-8') as f:
        floristeria_geojson = json.load(f)
    
    with open("assets/geojsons/gift_souvenir.geojson", "r", encoding='utf-8') as f:
        gift_souvenir_geojson = json.load(f)
    
    with open("assets/geojsons/hobby.geojson", "r", encoding='utf-8') as f:
        hobby_geojson = json.load(f)
    
    with open("assets/geojsons/joyeria.geojson", "r", encoding='utf-8') as f:
        joyeria_geojson = json.load(f)
    
    with open("assets/geojsons/optica.geojson", "r", encoding='utf-8') as f:
        optica_geojson = json.load(f)
    
    with open("assets/geojsons/pet_store.geojson", "r", encoding='utf-8') as f:
        pet_store_geojson = json.load(f)
    
    with open("assets/geojsons/calzado.geojson", "r", encoding='utf-8') as f:
        calzado_geojson = json.load(f)
    
    with open("assets/geojsons/used_merchandise.geojson", "r", encoding='utf-8') as f:
        used_merchandise_geojson = json.load(f)
    
    with open("assets/geojsons/medical_orthopedic.geojson", "r", encoding='utf-8') as f:
        medical_orthopedic_geojson = json.load(f)

    consumergoods_layers = [
        {"label": "Book Store", "value": "libreria", "geojson": libreria_geojson,"checked": False},
        {"label": "Clothing Store", "value": "tiendas_ropa", "geojson": tiendas_ropa_geojson,"checked": False},
        {"label": "Cosmetics Retail", "value": "cosmeticos", "geojson": cosmeticos_geojson,"checked": False},
        {"label": "Bazar & Department Store", "value": "bazar", "geojson": bazar_geojson,"checked": False},
        {"label": "Florist", "value": "floristeria", "geojson": floristeria_geojson,"checked": False},
        {"label": "Gift and Souvenir", "value": "gift_souvenir", "geojson": gift_souvenir_geojson,"checked": False},
        {"label": "Hobby Retailers", "value": "hobby", "geojson": hobby_geojson,"checked": False},
        {"label": "Jewelry Stores", "value": "joyeria", "geojson": joyeria_geojson,"checked": False},
        {"label": "Optical Goods", "value": "optica", "geojson": optica_geojson,"checked": False},
        {"label": "Pet Store", "value": "pet_store", "geojson": pet_store_geojson,"checked": False},
        {"label": "Shoe Store", "value": "calzado", "geojson": calzado_geojson,"checked": False},
        {"label": "Used Merchandise", "value": "used_merchandise", "geojson": used_merchandise_geojson,"checked": False},
        {"label": "Medical & Orthopedic Supply", "value": "medical_orthopedic", "geojson": medical_orthopedic_geojson,"checked": False},
    ]

    # DURABLE GOODS GEOJSONS
    with open("assets/geojsons/vehicle_dealer.geojson", "r", encoding='utf-8') as f:
        vehicle_dealer_geojson = json.load(f)
    
    with open("assets/geojsons/home_goods.geojson", "r", encoding='utf-8') as f:
        home_goods_geojson = json.load(f)
    
    with open("assets/geojsons/wholesale.geojson", "r", encoding='utf-8') as f:
        wholesale_geojson = json.load(f)

    durablegoods_layers = [
        {"label": "Car Dealer", "value": "vehicle_dealer", "geojson": vehicle_dealer_geojson,"checked": False},
        {"label": "Home Goods Store", "value": "home_goods", "geojson": home_goods_geojson,"checked": False},
        {"label": "Wholesale Trade", "value": "wholesale", "geojson": wholesale_geojson,"checked": False},
    ]

    # GROCERY GEOJSONS
    with open("assets/geojsons/convenience.geojson", "r", encoding='utf-8') as f:
        convenience_geojson = json.load(f)
    
    with open("assets/geojsons/supermercados_locales.geojson", "r", encoding='utf-8') as f:
        supermercados_locales_geojson = json.load(f)
    
    with open("assets/geojsons/hipermercados.geojson", "r", encoding='utf-8') as f:
        hipermercados_geojson = json.load(f)
    
    with open("assets/geojsons/specialty_food.geojson", "r", encoding='utf-8') as f:
        specialty_food_geojson = json.load(f)

    grocery_layers = [
        {"label": "Convenience Corner Store", "value": "convenience", "geojson": convenience_geojson,"checked": False},
        {"label": "Local Supermarket", "value": "supermercados_locales", "geojson": supermercados_locales_geojson,"checked": False},
        {"label": "Supermarket & Hypermarket", "value": "hipermercados", "geojson": hipermercados_geojson,"checked": False},
        {"label": "Specialty Food Retailers", "value": "specialty_food", "geojson": specialty_food_geojson,"checked": False},
    ]

    # CULTURAL GEOJSONS
    with open("assets/geojsons/galerias_arte.geojson", "r", encoding='utf-8') as f:
        galerias_arte_geojson = json.load(f)
    
    with open("assets/geojsons/biblioteca.geojson", "r", encoding='utf-8') as f:
        biblioteca_geojson = json.load(f)
    
    with open("assets/geojsons/museo.geojson", "r", encoding='utf-8') as f:
        museo_geojson = json.load(f)

    cultural_layers = [
        {"label": "Art Gallery", "value":"galerias_arte", "geojson":galerias_arte_geojson,"checked": False},
        {"label": "Library", "value":"biblioteca", "geojson":biblioteca_geojson,"checked": False},
        {"label": "Museum", "value":"museo", "geojson":museo_geojson,"checked": False},
    ]

    # ENTERTAINMENT GEOJSONS
    with open("assets/geojsons/parques_atracc.geojson", "r", encoding='utf-8') as f:
        parques_atracc_geojson = json.load(f)
    
    with open("assets/geojsons/azar.geojson", "r", encoding='utf-8') as f:
        azar_geojson = json.load(f)
    
    with open("assets/geojsons/cine.geojson", "r", encoding='utf-8') as f:
        cine_geojson = json.load(f)
    
    with open("assets/geojsons/artes_escenicas.geojson", "r", encoding='utf-8') as f:
        artes_escenicas_geojson = json.load(f)
    
    with open("assets/geojsons/spectator_sports.geojson", "r", encoding='utf-8') as f:
        spectator_sports_geojson = json.load(f)
    
    with open("assets/geojsons/parques_naturales.geojson", "r", encoding='utf-8') as f:
        parques_naturales_geojson = json.load(f)
    
    with open("assets/geojsons/parks.geojson", "r", encoding='utf-8') as f:
        parks_geojson = json.load(f)
    
    with open("assets/geojsons/playground.geojson", "r", encoding='utf-8') as f:
        playground_geojson = json.load(f)
    
    with open("assets/geojsons/playas.geojson", "r", encoding='utf-8') as f:
        playas_geojson = json.load(f)

    entertainment_layers = [
        {"label": "Amusement Park", "value":"parques_atracc", "geojson":parques_atracc_geojson,"checked": False},
        {"label": "Casino", "value":"azar", "geojson":azar_geojson,"checked": False},
        {"label": "Movie Theater", "value":"cine", "geojson":cine_geojson,"checked": False},
        {"label": "Performing Arts", "value":"artes_escenicas", "geojson":artes_escenicas_geojson,"checked": False},
        {"label": "Spectator Sports", "value":"spectator_sports", "geojson":spectator_sports_geojson,"checked": False},
        {"label": "Nature Parks", "value":"parques_naturales", "geojson":parques_naturales_geojson,"checked": False},
        {"label": "Parks and Gardens", "value":"parks", "geojson":parks_geojson,"checked": False},
        {"label": "Kids Playgrounds", "value":"playground", "geojson":playground_geojson,"checked": False},
        {"label": "Beaches", "value":"playas", "geojson":playas_geojson,"checked": False},
    ]

    # LEISURE & WELLNESS GEOJSONS
    with open("assets/geojsons/campos_golf.geojson", "r", encoding='utf-8') as f:
        campos_golf_geojson = json.load(f)
    
    with open("assets/geojsons/gym.geojson", "r", encoding='utf-8') as f:
        gym_geojson = json.load(f)
    
    with open("assets/geojsons/marina.geojson", "r", encoding='utf-8') as f:
        marina_geojson = json.load(f)
    
    with open("assets/geojsons/instalaciones_deportivas.geojson", "r", encoding='utf-8') as f:
        instalaciones_deportivas_geojson = json.load(f)

    leisurewellness_layers = [
        {"label": "Golf Courses", "value": "campos_golf", "geojson":campos_golf_geojson,"checked": False},
        {"label": "Gym", "value": "gym", "geojson":gym_geojson,"checked": False},
        {"label": "Marinas", "value": "marina", "geojson":marina_geojson, "checked": False},
        {"label": "Sports Recreation", "value": "instalaciones_deportivas", "geojson":instalaciones_deportivas_geojson,"checked": False},
    ]

    # TRANSPORT GEOJSONS
    with open("assets/geojsons/euskotren.geojson", "r", encoding='utf-8') as f:
        euskotren_geojson = json.load(f)
    
    with open("assets/geojsons/renfe.geojson", "r", encoding='utf-8') as f:
        renfe_geojson = json.load(f)
    
    with open("assets/geojsons/renfe_cercanias.geojson", "r", encoding='utf-8') as f:
        renfe_cercanias_geojson = json.load(f)
    
    with open("assets/geojsons/urban.geojson", "r", encoding='utf-8') as f:
        urban_geojson = json.load(f)
    
    with open("assets/geojsons/interurban.geojson", "r", encoding='utf-8') as f:
        interurban_geojson = json.load(f)
    
    with open("assets/geojsons/dbizi.geojson", "r", encoding='utf-8') as f:
        dbizi_geojson = json.load(f)
    
    with open("assets/geojsons/bike_parking.geojson", "r", encoding='utf-8') as f:
        bike_parking_geojson = json.load(f)
    
    with open("assets/geojsons/religious_catholic.geojson", "r", encoding='utf-8') as f:
        religious_catholic_geojson = json.load(f)
    
    with open("assets/geojsons/religious_other.geojson", "r", encoding='utf-8') as f:
        religious_other_geojson = json.load(f)

    train_layers = [
        {"label": "Euskotren", "value": "euskotren", "geojson":euskotren_geojson,"checked": False},
        {"label": "Train Stops (Renfe)", "value": "renfe", "geojson":renfe_geojson,"checked": False},
        {"label": "Regional Train Stops (Renfe Cercanías)", "value": "renfe_cercanias", "geojson":renfe_cercanias_geojson,"checked": False},
    ]

    bus_layers=[
        {"label": "Urban Bus Stops", "value": "urban", "geojson":urban_geojson,"checked": False},
        {"label": "Interurban Bus Stops", "value": "interurban", "geojson":interurban_geojson,"checked": False},
    ]

    bike_layers=[
        {"label": "DBizi Stops", "value": "dbizi", "geojson":dbizi_geojson,"checked": False},
        {"label": "Bike Parking", "value": "bike_parking", "geojson":bike_parking_geojson,"checked": False},
    ]

    religious_layers = [
        {"label": "Catholic Religious Centers", "value": "religious_catholic", "geojson":religious_catholic_geojson,"checked": False},
        {"label": "Other Religious Centers", "value": "religious_other", "geojson":religious_other_geojson,"checked": False},
    ]

    # Combined for other uses
    all_layers = [
            eat_layers, school_layers, healthcare_layers, leisure_layers, professional_layers,
            pharmacy_layers, service_layers, hotel_layers, consumergoods_layers,
            durablegoods_layers, grocery_layers, cultural_layers, entertainment_layers,
            leisurewellness_layers, train_layers, bus_layers, bike_layers, religious_layers
        ]

    layer_labels = {}

    # Iterate through each group of layers in all_layers
    for layer_group in all_layers:
        for layer in layer_group:
            # Ensure the layer contains the 'value' and 'label' keys
            if "value" in layer and "label" in layer:
                layer_labels[layer["value"]] = layer["label"]

    poi_menu = html.Div(
        dbc.Accordion(
            [
                # Eat Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            html.H6("Food & Beverage", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "eat-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "10px"}
                                )
                                for i, item in enumerate(eat_layers)
                            ])
                        ]
                    ),
                    title="Eat",
                    item_id="eatery",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # School Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            html.H6("Education", style={"marginTop": "10px", "marginBottom": "5px"}),
                            html.Div([
                                dmc.Checkbox(
                                    id={"type": "education-item", "index": i},
                                    label=item["label"],
                                    checked=item["checked"],
                                    style={"marginTop": "5px", "marginLeft": "10px"}
                                )
                                for i, item in enumerate(school_layers)
                            ])
                        ]
                    ),
                    title="School",
                    item_id="school",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # Errands Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            # Healthcare
                            html.Div([
                                html.H6("Healthcare", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "healthcare-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(healthcare_layers)
                                ])
                            ]),
                            # Leisure
                            html.Div([
                                html.H6("Leisure & Wellness", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "leisure-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(leisure_layers)
                                ])
                            ]),
                            # Professional Services
                            html.Div([
                                html.H6("Professional Services", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "professional-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(professional_layers)
                                ])
                            ]),
                            # Retail (Pharmacy)
                            html.Div([
                                html.H6("Retail (Pharmacy)", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "pharmacy-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(pharmacy_layers)
                                ])
                            ]),
                            # Service
                            html.Div([
                                html.H6("Service", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "service-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(service_layers)
                                ])
                            ]),
                        ]
                    ),
                    title="Errands",
                    item_id="errands",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # Lodging Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            # Hotel
                            html.Div([
                                html.H6("Hotel", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "hotel-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(hotel_layers)
                                ])
                            ]),
                        ]
                    ),
                    title="Lodging",
                    item_id="lodging",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # Shop Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            # Retail (Consumer Goods)
                            html.Div([
                                html.H6("Consumer Goods", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "consumergoods-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(consumergoods_layers)
                                ])
                            ]),
                            # Retail (Durable Goods)
                            html.Div([
                                html.H6("Durable Goods", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "durablegoods-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(durablegoods_layers)
                                ])
                            ]),
                            # Retail (Grocery)
                            html.Div([
                                html.H6("Grocery", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "grocery-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(grocery_layers)
                                ])
                            ]),
                        ]
                    ),
                    title="Shop",
                    item_id="shop",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # Recreation Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            # Cultural
                            html.Div([
                                html.H6("Cultural", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "cultural-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(cultural_layers)
                                ])
                            ]),
                            # Entertainment
                            html.Div([
                                html.H6("Entertainment", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "entertainment-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(entertainment_layers)
                                ])
                            ]),
                            # Leisure & Wellness
                            html.Div([
                                html.H6("Leisure & Wellness", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "leisurewellness-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(leisurewellness_layers)
                                ])
                            ]),
                        ]
                    ),
                    title="Recreation",
                    item_id="recreation",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # Transport Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            # Train
                            html.Div([
                                html.H6("Train", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "train-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(train_layers)
                                ])
                            ]),
                            # Bus
                            html.Div([
                                html.H6("Bus", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "bus-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(bus_layers)
                                ])
                            ]),
                            # Bike
                            html.Div([
                                html.H6("Bike", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "bike-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "5px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(bike_layers)
                                ])
                            ]),
                        ]
                    ),
                    title="Transport",
                    item_id="transport",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
                # Errands Section
                dbc.AccordionItem(
                    html.Div(
                        children=[
                            # Religious
                            html.Div([
                                html.H6("Religious", style={"marginTop": "10px", "marginBottom": "5px"}),
                                html.Div([
                                    dmc.Checkbox(
                                        id={"type": "religious-item", "index": i},
                                        label=item["label"],
                                        checked=item["checked"],
                                        style={"marginTop": "0px", "marginLeft": "33px"}
                                    )
                                    for i, item in enumerate(religious_layers)
                                ])
                            ]),
                        ]
                    ),
                    title="Others",
                    item_id="others",
                    style={  # Apply style here
                        "maxHeight": "150px",  # Adjust as needed
                        "overflowY": "auto",  # Scrollbar only when necessary
                    },
                ),
            ],
            id="accordion",
            active_item="eat",
        ),
        style={
            "backgroundColor": "rgba(255, 255, 255, 0.9)",
            "padding": "2px",
            "borderRadius": "5px",
            "width": "360px",
        },
    )

    data_mt = [["walk", "Walk"], ["bike", "Bike"], ["pt", "Public Transit"], ["car", "Car"]]

    # Define the first radio group as a separate component
    mt_menu = html.Div(
        children=[
            dmc.RadioGroup(
                children=dmc.Group(
                    [dmc.Radio(label, value=value) for value, label in data_mt],
                my=10,
                ),
                id="transport-choice",
                value="walk",
                label="Select a mode of transport",
                size="sm",
            )
        ]
    )

    data_demog = [["total_women", "Female Population Density"], ["choiceB", "Foreign Population"], ["choiceC", "Income Level"]]

    # Define the second radio group as a separate component
    demog_menu = html.Div(
        children=[
            dmc.RadioGroup(
                children=dmc.Stack(
                    [dmc.Radio(label, value=value) for value, label in data_demog],
                    my=10,
                ),
                id="demographics-choice",
                value=None,
                label="Select the demographic data to display",
                size="sm",
                mb=10,
            )
        ]
    )

    buttons = html.Div(
        children=[
            dmc.Group([
            dmc.Button("Apply", variant="filled", size="md", id="apply-button"),
            dmc.Button("Reset", variant="filled", size="md", id="reset-button"),
        ],
            id="button-group",
            gap=40,
            justify="center",
        )
        ]
    )

    # Define map and data
    classes = [0, 3, 6, 10, 15, 20, 25]
    colorscale = ['#00572a', '#7CB342', '#FFFF00', '#FFA500', '#D50000', '#8f0340', '#6a1717']

    # Define categories for color bar
    ctg = [f"{cls}-{classes[i + 1]}" for i, cls in enumerate(classes[:-1])] + [f"{classes[-1]}+"]
    colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomright")

    buttons_comarcas = html.Div(
        children=[
            dmc.Group([
            dmc.Button("Donostialdea", variant="filled", size="md", id="donostia-button"),
            dmc.Button("Debabarrena", variant="filled", size="md", id="debab-button"),
            dmc.Button("Debagoiena", variant="filled", size="md", id="debag-button"),
            dmc.Button("Bidasoaldea", variant="filled", size="md", id="bidasoa-button"),
            dmc.Button("Goierri", variant="filled", size="md", id="goierri-button"),
            dmc.Button("Urola Kosta", variant="filled", size="md", id="urolak-button"),
            dmc.Button("Tolosaldea", variant="filled", size="md", id="tolosa-button"),
        ],
            id="buttons-comarca",
            gap=20,
            justify="center",
        )
        ]
    )

    # Layout
    app.layout = dmc.MantineProvider(html.Div(
        [
            # Map Component
            dl.Map(
                [
                    dl.TileLayer(url='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', maxZoom=20),
                    dl.GeoJSON(
                        id="geojson-layer",
                        data=geojson,  # Replace with your actual endpoint
                        options=dict(style=visual_style, onEachFeature=on_each_feature),
                    ),
                    dl.LayerGroup(id="map-points"),
                    colorbar,
                    dl.ZoomControl(position="bottomright", id="zoom"),
                ],
                center=[43.16, -2.2],
                zoom=11,
                style={"height": "100vh", "width": "100%"},
                zoomControl=False,  # Disable default zoom control
                id="map",
            ),
            # Sidebar Container
            html.Div(
                [
                    # All Menus in One Container
                    html.Div(
                        [
                            html.Div(
                                mt_menu,
                                style={
                                    "marginBottom": "2px",
                                    "padding": "10px",
                                    "backgroundColor": "white",
                                    "borderRadius": "5px",
                                },
                            ),
                            html.Div(
                                poi_menu,
                            ),
                            html.Div(
                                demog_menu,
                                style={
                                    "marginBottom": "2px",
                                    "padding": "10px",
                                    "backgroundColor": "white",
                                    "borderRadius": "5px",

                                },
                            ),
                            html.Div(
                                buttons,
                                style={

                                    "borderRadius": "5px",
                                    "backgroundColor": "rgba(255, 255, 255)",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "2px",  # Space between menus
                        },
                    ),
                ],
                style={
                    "position": "absolute",
                    "top": "10px",
                    "left": "10px",
                    "width": "380px",
                    "backgroundColor": "rgba(255, 255, 255)",
                    "zIndex": 1000,
                    "padding": "10px",
                    "borderRadius": "5px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                },
            ),
            info,
            dcc.Store(id="selected-pois", data=[]),  # Store for POIs (empty list as default),
            dcc.Interval(id='interval', interval=1000),
            html.Div(
                [
                    buttons_comarcas,
                ],
                style={
                    "position": "absolute",
                    "top": "10px",
                    "left": "350px",
                    "width": "1200px",
                    "zIndex": 1000,
                    "padding": "10px",
                    "borderRadius": "5px",

                },
            ),
        ]
    ))

    # Update the callback to display the hovered feature's information, including CUSEC
    @callback(
        Output("info", "children"),  # Update the info display
        [Input("geojson-layer", "hoverData"),  # Trigger when hovering over GeoJSON layer
        Input("selected-pois", "data"),  # Access selected POIs from the dcc.Store
        State("transport-choice", "value")]  # Access selected transport mode from the dcc.Store
    )
    def info_hover(feature, selected_pois, transport_mode):
        print("Feature:", feature)
        print("Selected POIs:", selected_pois)
        print("Transport Mode:", transport_mode)

        # Use the feature and selected_pois data in your function
        return get_info(feature, selected_pois, transport_mode)


    @app.callback(
        [
            Output("geojson-layer", "data"),  # Update GeoJSON layer
            Output("map-points", "children"),  # Update map points
            Output("selected-pois", "data"),  # Update selected POIs in the Store
            Output("transport-choice", "value"),  # Reset transport choice
            Output({"type": ALL, "index": ALL}, "checked"),  # Reset POI checkboxes
            Output("demographics-choice", "value"),  # Reset demographic choice
        ],
        [
            Input("apply-button", "n_clicks"),  # Trigger on Apply button click
            Input("reset-button", "n_clicks"),  # Trigger on Reset button click
        ],
        [
            State({"type": ALL, "index": ALL}, "checked"),  # Read checkbox states
            State("transport-choice", "value"),  # Read mode of transport selection
            State("demographics-choice", "value"),  # Read selected demographic group
        ],
        prevent_initial_call=True,
    )
    def handle_apply_or_reset(apply_clicks, reset_clicks, checked_values, transport_mode, selected_demographic):
        # Determine which button was clicked
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, [dash.no_update] * len(checked_values), dash.no_update

        triggered_id = ctx.triggered_id

        if triggered_id == "apply-button":
            # Logic for Apply button
            color_priority = ['#6a1717', '#8f0340', '#D50000', '#FFA500', '#FFFF00', '#7CB342', '#00572a']
            selected_pois = []
            map_points = []

            # Loop through layers and collect selected POIs and points
            layer_idx = 0
            for layer_group in all_layers:
                for idx, checked in enumerate(checked_values[layer_idx:layer_idx + len(layer_group)]):
                    if checked:
                        layer = layer_group[idx]
                        selected_pois.append(layer["value"])

                        for feature in layer["geojson"]["features"]:
                            coordinates = feature.get("geometry", {}).get("coordinates")
                            if coordinates and len(coordinates) >= 2:
                                lon, lat = coordinates
                                if lat is not None and lon is not None:
                                    map_points.append(
                                        dl.Marker(
                                            position=[lat, lon],
                                            children=[dl.Popup(layer["label"])],
                                            icon=custom_icon,
                                        )
                                    )
                layer_idx += len(layer_group)

            # Update projection features with selected colors, opacity, and demographic data
            for feature in projected_geojson['features']:
                feature_colors = []
                for column in selected_pois:
                    column_with_mode = f"{column}_{transport_mode}"
                    color = feature['properties'].get(column_with_mode)
                    if color in color_priority:
                        feature_colors.append(color)

                # Assign the highest priority color
                if feature_colors:
                    selected_color = next((color for color in color_priority if color in feature_colors), '#676d70')
                    feature['properties']['color'] = selected_color
                else:
                    feature['properties']['color'] = '#676d70'
            
            column_with_mode_list = [f"{col}_{transport_mode}" for col in selected_pois]
            # Seleccionamos solo las columnas relevantes para la referencia
            selected_df = buildings_df[column_with_mode_list].copy()
            print(selected_df.head())  # Ver las primeras filas del DataFrame

            # Paso 2: Filtrar las columnas de color prioritario
            # Creamos una función para determinar el color basado en la prioridad
            def get_color(row):
                if len(selected_pois) > 1:
                    # Si hay más de un POI, recorremos las columnas y seleccionamos el primero que esté en color_priority
                    for column in row.index:  # Iterar sobre las columnas
                        color = row[column]
                        if pd.notna(color) and color in color_priority:
                            return color
                    return None
                else:
                    color = row[column_with_mode_list[0]]  # Seleccionamos la columna correspondiente al POI
                    return color

            # Aplicamos la función fila por fila
            selected_df.loc[:, 'color'] = selected_df.apply(get_color, axis=1)

            # Paso 3: Crear el DataFrame final con Referencia y color
            # Obtenemos la 'Referencia' del DataFrame original
            final_df = buildings_df[['Referencia']].join(selected_df['color'])
            print(final_df.head()) 

            # Finalmente, seleccionamos solo las filas con un color válido
            final_df['color'] = final_df['color'].fillna('#6baed6')
            color_dict = final_df.set_index('Referencia')['color'].to_dict()

            # Update GeoJSON features with selected colors, opacity, and demographic data
            for feature in geojson['features']:
                feature_id = feature['properties']['Referencia']
                # Asignamos el color basado en la referencia, si existe
                feature['properties']['selectedColor'] = color_dict.get(feature_id, '#6baed6')

                # Handle demographic opacity if a demographic is selected
                if selected_demographic:
                    opacity_column = f"{selected_demographic}"
                    opacity = feature['properties'].get(opacity_column)
                    if opacity is not None:
                        feature['properties']['selectedOpacity'] = opacity
                    else:
                        feature['properties']['selectedOpacity'] = 0.4  # Default value if opacity is not found
                else:
                    feature['properties']['selectedOpacity'] = 0.4  # Default opacity if no demographic selected

            cityio.send_geojson(projected_geojson)
            return geojson, map_points, selected_pois, transport_mode, [dash.no_update] * len(checked_values), selected_demographic

        elif triggered_id == "reset-button":
            # Reset button logic
            default_transport_mode = "walk"  # Replace with your default value for transport mode
            default_checkboxes = [False] * len(checked_values)
            default_demographic = None  # Reset demographic choice

            # Clear `selectedColor` and `selectedOpacity` for all features in the GeoJSON
            for feature in geojson['features']:
                feature['properties']['selectedColor'] = None  # Or replace with a neutral default color
                feature['properties']['selectedOpacity'] = 0.4  # Reset opacity to default

            for feature in projected_geojson['features']:
                feature['properties']['color'] = '#6baed6'  # Or replace with a neutral default color

            cityio.send_geojson(projected_geojson)
            # Clear map points and reset controls
            return geojson, [], [], default_transport_mode, default_checkboxes, default_demographic

    """
    @app.callback(
        Output("map", "viewport"),
        [
            Input("donostia-button", "n_clicks"),
            Input("debab-button", "n_clicks"),
            Input("debag-button", "n_clicks"),
            Input("bidasoa-button", "n_clicks"),
            Input("goierri-button", "n_clicks"),
            Input("urolak-button", "n_clicks"),
            Input("tolosa-button", "n_clicks"),
        ],
        prevent_initial_call=True
    )
    def fly_to_region(*_):
        button_id = ctx.triggered_id  # Gets the ID of the button that triggered the callback

        if button_id == "donostia-button":
            return dict(center=[43.289754, -1.986536], zoom=13, transition="flyTo")
        elif button_id == "debab-button":
            return dict(center=[43.245188, -2.378489], zoom=13, transition="flyTo")
        elif button_id == "debag-button":
            return dict(center=[43.064501, -2.454893], zoom=13, transition="flyTo")
        elif button_id == "bidasoa-button":
            return dict(center=[43.339777, -1.800981], zoom=13, transition="flyTo")
        elif button_id == "goierri-button":
            return dict(center=[43.022608, -2.241060], zoom=13, transition="flyTo")
        elif button_id == "urolak-button":
            return dict(center=[43.237423, -2.207675], zoom=13, transition="flyTo")
        elif button_id == "tolosa-button":
            return dict(center=[43.134334, -2.075681], zoom=13, transition="flyTo")
        return dash.no_update  # Fallback in case no button was clicked
    """

    @app.callback(
        Output("map", "viewport"),
        [
            Input("donostia-button", "n_clicks"),
            Input("debab-button", "n_clicks"),
            Input("debag-button", "n_clicks"),
            Input("bidasoa-button", "n_clicks"),
            Input("goierri-button", "n_clicks"),
            Input("urolak-button", "n_clicks"),
            Input("tolosa-button", "n_clicks"),
        ],
        prevent_initial_call=True
    )
    def fly_to_region(*_):
        #button_id = ctx.triggered_id  # Gets the ID of the button that triggered the callback
        #print(ctx.triggered)
        triggered_values = ctx.triggered
        for i_comarcas in triggered_values:
            if i_comarcas['prop_id'] == 'donostia-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.289754, -1.986536], zoom=13, transition="flyTo")
            elif i_comarcas['prop_id'] == 'debab-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.245188, -2.378489], zoom=13, transition="flyTo")
            elif i_comarcas['prop_id'] == 'debag-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.064501, -2.454893], zoom=13, transition="flyTo")
            elif i_comarcas['prop_id'] == 'bidasoa-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.339777, -1.800981], zoom=13, transition="flyTo")
            elif i_comarcas['prop_id'] == 'goierri-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.022608, -2.241060], zoom=13, transition="flyTo")
            elif i_comarcas['prop_id'] == 'urolak-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.237423, -2.207675], zoom=13, transition="flyTo")
            elif i_comarcas['prop_id'] == 'tolosa-button.n_clicks' and i_comarcas['value'] == 1:
                return dict(center=[43.134334, -2.075681], zoom=13, transition="flyTo")
        return dash.no_update  # Fallback in case no button was clicked


    app.run_server(debug=False)

if __name__ == "__main__":
    freeze_support()
    main()
    
