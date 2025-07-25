import requests
import json
import csv
import time
import os
import math

from dotenv import load_dotenv

load_dotenv()

# Carga tu API Key desde una variable de entorno (usa dotenv si prefieres)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Validar que la API Key esté presente
if not API_KEY:
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada. Por favor, crea un archivo .env o configúrala.")
    exit()

print(f"API Key cargada: {'*' * (len(API_KEY) - 4) + API_KEY[-4:] if API_KEY else 'N/A'}")

# --- MODIFICACIÓN CLAVE AQUÍ ---
# Definir una lista que contiene SOLO el nuevo cuadro delimitador
BOUNDING_BOXES = [
    {   # The new bounding box you provided
        "MIN_LATITUDE": 15.811151532248132,  # The lowest latitude
        "MAX_LATITUDE": 15.826402656043086,   # The highest latitude
        "MIN_LONGITUDE": -97.03805489890463, # The westernmost longitude (most negative)
        "MAX_LONGITUDE": -97.02703729905424   # The easternmost longitude (least negative)
    }
]
# --- FIN DE LA MODIFICACIÓN ---

# Tamaño de cada celda de la cuadrícula y radio de búsqueda
SEARCH_RADIUS_METERS = 500
GRID_STEP_METERS = 400

# Tipos de comercios a buscar
PLACE_TYPES = [
    "restaurant", "store", "supermarket", "cafe", "bar", "pharmacy",
    "clothing_store", "hardware_store", "convenience_store",
    "gym", "lodging"
]
# Nombre del archivo CSV de salida
OUTPUT_CSV_FILE = "comercios_puerto_escondido_cuadro_especifico.csv"

# Constantes para la conversión de grados a metros
EARTH_RADIUS_METERS = 6371000

def meters_to_degrees_latitude(meters):
    """Convierte metros a grados de latitud."""
    return meters / EARTH_RADIUS_METERS * (180 / math.pi)

def meters_to_degrees_longitude(meters, latitude):
    """Convierte metros a grados de longitud en una latitud dada."""
    return meters / (EARTH_RADIUS_METERS * math.cos(math.radians(latitude))) * (180 / math.pi)

def search_nearby_places(latitude, longitude, radius, place_type, api_key, page_token=None):
    """
    Realiza una solicitud a la Places API (New) SearchNearby.
    """
    url = "https://places.googleapis.com/v1/places:searchNearby"

    field_mask = "places.displayName,places.formattedAddress,places.location,places.primaryType,places.types,places.id"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": field_mask
    }

    payload = {
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius
            }
        },
        "includedTypes": [place_type],
    }

    if page_token:
        payload["pageToken"] = page_token

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al consultar {place_type} en ({latitude:.4f}, {longitude:.4f}): {http_err}")
        print(f"Respuesta del servidor: {response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Error de conexión/petición al consultar {place_type} en ({latitude:.4f}, {longitude:.4f}): {req_err}")
        return None

def load_existing_places(filename):
    """Carga los comercios existentes desde un archivo CSV."""
    existing_places = {}
    if os.path.exists(filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                required_columns = ["Nombre", "Tipo de comercio", "Latitud", "Longitud", "Direccion completa"]
                # Mejoramos la verificación de columnas para que sea más robusta a cambios futuros
                if not all(col in reader.fieldnames for col in required_columns):
                    print(f"Advertencia: El archivo CSV existente '{filename}' no tiene todas las columnas esperadas. Se creará uno nuevo o se sobrescribirá si no hay datos nuevos.")
                    return {}
                for row in reader:
                    # Usamos el place_id si existe, si no, la heurística.
                    place_id = row.get('id')
                    place_key = place_id if place_id else (
                        row.get("Nombre", "").strip().lower(),
                        float(row.get("Latitud", 0.0)) if isinstance(row.get("Latitud"), (int, float, str)) and str(row.get("Latitud")).replace('.', '', 1).isdigit() else 0.0,
                        float(row.get("Longitud", 0.0)) if isinstance(row.get("Longitud"), (int, float, str)) and str(row.get("Longitud")).replace('.', '', 1).isdigit() else 0.0
                    )
                    existing_places[place_key] = row
            print(f"Cargados {len(existing_places)} comercios existentes de '{filename}'.")
        except Exception as e:
            print(f"Error al leer el archivo CSV existente '{filename}': {e}. Se comenzará con una lista vacía.")
            existing_places = {}
    return existing_places

def main():
    # Cargar comercios existentes al inicio
    all_places = load_existing_places(OUTPUT_CSV_FILE)
    initial_places_count = len(all_places)
    new_places_found_this_run = 0

    print(f"Iniciando búsqueda de comercios en {len(BOUNDING_BOXES)} cuadro(s) específico(s) de Puerto Escondido.")
    print(f"Radio de búsqueda por celda: {SEARCH_RADIUS_METERS} metros")
    print(f"Paso de cuadrícula: {GRID_STEP_METERS} metros")
    print(f"Tipos de comercio a buscar: {', '.join(PLACE_TYPES)}")

    # Iterar solo sobre el cuadro delimitador especificado
    for i, bbox in enumerate(BOUNDING_BOXES):
        MIN_LATITUDE = bbox["MIN_LATITUDE"]
        MAX_LATITUDE = bbox["MAX_LATITUDE"]
        MIN_LONGITUDE = bbox["MIN_LONGITUDE"]
        MAX_LONGITUDE = bbox["MAX_LONGITUDE"]

        print(f"\n--- Procesando Cuadro Delimitador {i+1}/{len(BOUNDING_BOXES)} ---")
        print(f"Límites: Latitud [{MIN_LATITUDE}, {MAX_LATITUDE}], Longitud [{MIN_LONGITUDE}, {MAX_LONGITUDE}]")

        # Calcula los pasos en grados para la cuadrícula para el bbox actual
        lat_step_degrees = meters_to_degrees_latitude(GRID_STEP_METERS)

        # Itera sobre la cuadrícula dentro del bbox actual
        current_lat = MIN_LATITUDE
        while current_lat <= MAX_LATITUDE:
            lon_step_degrees = meters_to_degrees_longitude(GRID_STEP_METERS, current_lat)
            current_lon = MIN_LONGITUDE
            while current_lon <= MAX_LONGITUDE:
                print(f"\n  Procesando celda en Lat: {current_lat:.4f}, Lon: {current_lon:.4f}...")

                for place_type in PLACE_TYPES:
                    print(f"    Buscando tipo de comercio: '{place_type}'...")
                    page_token = None
                    type_count_in_cell = 0

                    # Bucle de paginación para cada tipo y celda
                    while True:
                        response_data = search_nearby_places(
                            current_lat,
                            current_lon,
                            SEARCH_RADIUS_METERS,
                            place_type,
                            API_KEY,
                            page_token
                        )

                        if response_data and "places" in response_data:
                            for place in response_data["places"]:
                                place_id = place.get('id')
                                name = place.get('displayName', {}).get('text', 'N/A')
                                place_types_list = place.get('types', [])
                                main_type = place_types_list[0] if place_types_list else 'N/A'
                                latitude = place.get('location', {}).get('latitude', 'N/A')
                                longitude = place.get('location', {}).get('longitude', 'N/A')
                                full_address = place.get('formattedAddress', 'N/A')

                                # Usar el place_id de Google como la clave principal para evitar duplicados
                                unique_key = place_id if place_id else (
                                    name.strip().lower(),
                                    float(latitude) if isinstance(latitude, (int, float)) else (float(latitude) if str(latitude).replace('.', '', 1).isdigit() else 0.0),
                                    float(longitude) if isinstance(longitude, (int, float)) else (float(longitude) if str(longitude).replace('.', '', 1).isdigit() else 0.0)
                                )

                                if unique_key not in all_places:
                                    all_places[unique_key] = {
                                        "Nombre": name,
                                        "Tipo de comercio": main_type,
                                        "Latitud": latitude,
                                        "Longitud": longitude,
                                        "Direccion completa": full_address,
                                        "id": place_id # Guardar el ID de Google para mejor deduplicación futura
                                    }
                                    new_places_found_this_run += 1
                                    type_count_in_cell += 1

                            page_token = response_data.get("nextPageToken")
                            if page_token:
                                print(f"      Obteniendo siguiente página para '{place_type}'...")
                                time.sleep(1.5)
                            else:
                                print(f"      Finalizada búsqueda para '{place_type}'. Nuevos en celda para tipo: {type_count_in_cell}.")
                                break
                        else:
                            print(f"      No se encontraron más resultados para '{place_type}' en esta celda o hubo un error.")
                            break

                current_lon += lon_step_degrees
                time.sleep(0.5)
            current_lat += lat_step_degrees

    # Guardar los datos en un archivo CSV
    if all_places:
        print(f"\n--- Resumen de la Ejecución ---")
        print(f"Comercios existentes cargados al inicio: {initial_places_count}")
        print(f"Nuevos comercios encontrados en esta ejecución: {new_places_found_this_run}")
        print(f"Total de comercios únicos en el CSV: {len(all_places)}")

        csv_columns = ["Nombre", "Tipo de comercio", "Latitud", "Longitud", "Direccion completa", "id"]
        try:
            with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for place_data in all_places.values():
                    row_to_write = {col: place_data.get(col, '') for col in csv_columns}
                    writer.writerow(row_to_write)
            print(f"Datos actualizados exitosamente en '{OUTPUT_CSV_FILE}'")
        except IOError:
            print(f"Error al escribir en el archivo CSV '{OUTPUT_CSV_FILE}'")
    else:
        print("No se encontraron comercios para guardar.")

if __name__ == "__main__":
    main()