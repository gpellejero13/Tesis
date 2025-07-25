import pandas as pd
import folium

import pandas as pd
from io import StringIO

def get_color_by_supertypo(tipo_comercio):
    """
    Recibe un tipo de comercio y retorna el color asociado a su supertipo.

    Args:
        tipo_comercio (str): El tipo de comercio (ej. 'restaurant', 'hotel').

    Returns:
        str: El color del supertipo (ej. 'red', 'green', 'purple', 'orange').
             Retorna 'gray' si el supertipo o el tipo de comercio no se encuentra.
    """
    # Mapeo de Tipo de comercio a Supertipo
    supertypes_mapping_data = """Tipo de comercio,Supertipo
american_restaurant,restaurante
apartment_building,hotel
apartment_complex,hotel
art_gallery,otro
asian_restaurant,restaurante
auto_parts_store,otro
bakery,restaurante
bar,restaurante
bar_and_grill,restaurante
barbecue_restaurant,restaurante
barber_shop,otro
bed_and_breakfast,hotel
body_art_service,otro
book_store,otro
breakfast_restaurant,restaurante
brunch_restaurant,restaurante
butcher_shop,otro
cafe,restaurante
cafeteria,restaurante
campground,otro
camping_cabin,otro
candy_store,otro
car_dealer,otro
car_rental,otro
cell_phone_store,otro
child_care_agency,otro
chinese_restaurant,restaurante
clothing_store,otro
coffee_shop,restaurante
condominium_complex,hotel
convenience_store,abarrotes
corporate_office,otro
cottage,otro
cultural_center,otro
deli,restaurante
department_store,otro
dessert_restaurant,restaurante
dessert_shop,restaurante
doctor,otro
drugstore,otro
electronics_store,otro
event_venue,otro
extended_stay_hotel,hotel
farm,otro
fast_food_restaurant,restaurante
fitness_center,otro
florist,otro
food,restaurante
food_court,restaurante
food_store,restaurante
french_restaurant,restaurante
furniture_store,otro
general_contractor,otro
gift_shop,otro
greek_restaurant,restaurante
grocery_store,abarrotes
guest_house,hotel
gym,otro
hamburger_restaurant,restaurante
hardware_store,otro
health,otro
home_goods_store,otro
home_improvement_store,otro
hostel,hotel
hotel,hotel
housing_complex,hotel
ice_cream_shop,restaurante
inn,otro
internet_cafe,restaurante
italian_restaurant,restaurante
japanese_restaurant,restaurante
jewelry_store,otro
juice_shop,restaurante
korean_restaurant,restaurante
liquor_store,restaurante
lodging,hotel
market,abarrotes
meal_delivery,restaurante
meal_takeaway,restaurante
mediterranean_restaurant,restaurante
mexican_restaurant,restaurante
motel,hotel
night_club,otro
pharmacy,otro
physiotherapist,otro
pizza_restaurant,restaurante
place_of_worship,otro
point_of_interest,otro
private_guest_room,hotel
pub,restaurante
resort_hotel,hotel
restaurant,restaurante
seafood_restaurant,restaurante
shoe_store,otro
shopping_mall,otro
spa,otro
sporting_goods_store,otro
sports_coaching,otro
sports_complex,otro
steak_house,restaurante
store,abarrotes
supermarket,abarrotes
sushi_restaurant,restaurante
swimming_pool,otro
thai_restaurant,restaurante
tour_agency,otro
vegan_restaurant,restaurante
vegetarian_restaurant,restaurante
veterinary_care,otro
wedding_venue,otro
wholesaler,otro
wine_bar,restaurante
yoga_studio,otro
"""
    # Convertir la cadena de texto a un DataFrame y luego a un diccionario
    supertypes_df = pd.read_csv(StringIO(supertypes_mapping_data))
    supertypes_map = supertypes_df.set_index("Tipo de comercio")["Supertipo"].to_dict()

    # Definir colores para cada Supertipo
    color_map = {
        "restaurante": "red",
        "hotel": "green",
        "abarrotes": "purple",
        "otro": "orange"
    }

    # Obtener el supertipo del tipo de comercio dado
    supertipo = supertypes_map.get(tipo_comercio, "otro")

    # Retornar el color correspondiente al supertipo
    return color_map.get(supertipo, "gray") # 'gray' como color por defecto si no se encuentra


def generate_html_map_from_csv(csv_file_path, output_html_file="mapa_comercios_puerto_escondido.html",
                               map_center_lat=15.8642, map_center_lon=-97.0691, initial_zoom=13):
    """
    Genera un archivo HTML con un mapa interactivo de OpenStreetMap.
    Los puntos se cargan desde un archivo CSV y muestran Nombre y Tipo de comercio como tooltip.

    Args:
        csv_file_path (str): Ruta al archivo CSV generado con los datos de los comercios.
        output_html_file (str): Nombre del archivo HTML de salida.
        map_center_lat (float): Latitud central inicial del mapa.
        map_center_lon (float): Longitud central inicial del mapa.
        initial_zoom (int): Nivel de zoom inicial del mapa (ej. 10 para vista general, 15 para vista detallada).
    """

    try:
        # Cargar los datos desde el CSV
        df = pd.read_csv(csv_file_path)
        print(f"CSV '{csv_file_path}' cargado exitosamente. Se encontraron {len(df)} comercios.")

        # Crear el objeto mapa centrado en Puerto Escondido
        m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=initial_zoom,
                       tiles="OpenStreetMap") # Puedes cambiar a 'CartoDB positron' para un estilo más claro

        # Añadir marcadores para cada comercio
        for index, row in df.iterrows():
            nombre = row["Nombre"]
            tipo_comercio = row["Tipo de comercio"]
            latitud = row["Latitud"]
            longitud = row["Longitud"]


            # Obtener el color basado en el Supertipo
            marker_color = get_color_by_supertypo(row["Tipo de comercio"])

            # marker_color = color_map.get(get_color_by_supertypo(row["Tipo de comercio"]), "gray")  # Por defecto, gris si no se encuentra el Supertipo

            # Crear el tooltip (la información que aparece al pasar el mouse o hacer clic)
            tooltip_text = f"<b>Nombre:</b> {nombre}<br><b>Tipo:</b> {tipo_comercio}"


            # --- MODIFICACIÓN CLAVE AQUÍ ---
            # Crear un ícono de círculo mucho más pequeño
            # radius: El tamaño del círculo. Un valor de 1 a 3 suele ser muy pequeño.
            # color: El color del círculo.
            # fill: Si el círculo debe estar relleno.
            # fill_color: El color de relleno.
            # fill_opacity: La transparencia del relleno.
            folium.CircleMarker(
                location=[latitud, longitud],
                radius=2,  # Ajusta este valor para controlar el tamaño (un valor de 1 a 3 es muy pequeño)
                color=marker_color, # Color del borde del círculo
                fill=True,
                fill_color=marker_color,  # Usar el color del Supertipo para el relleno
                fill_opacity=0.7,
                tooltip=tooltip_text,
                popup=folium.Popup(tooltip_text, max_width=300)
            ).add_to(m)
            # --- FIN DE LA MODIFICACIÓN ---


        # Guardar el mapa en un archivo HTML
        m.save(output_html_file)
        print(f"Mapa generado exitosamente en '{output_html_file}'")

    except FileNotFoundError:
        print(f"Error: El archivo CSV '{csv_file_path}' no fue encontrado.")
    except KeyError as e:
        print(f"Error: No se encontró la columna esperada en el CSV. Asegúrate de que las columnas 'Nombre', 'Tipo de comercio', 'Latitud', 'Longitud' existan. Falta la columna: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

