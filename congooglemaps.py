import googlemaps
import os
from dotenv import load_dotenv

# Cargar la clave desde el archivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Inicializar el cliente de Google Maps
gmaps = googlemaps.Client(key=api_key)

origen = "El Cafecito Zicatela, Puerto Escondido"
destino = "Dan's Café Deluxe, Puerto Escondido"

resultado = gmaps.distance_matrix(origen, destino, mode="walking", language="es")

distancia = resultado['rows'][0]['elements'][0]['distance']['text']
tiempo = resultado['rows'][0]['elements'][0]['duration']['text']

print(f"Distancia: {distancia}, Tiempo estimado: {tiempo}")

import requests

API_KEY = "AIzaSyAS-zRyJbMfoSEUGdEc5KyRZ78Kwyt9_Bw"

def obtener_coordenadas(nombre_lugar):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={nombre_lugar}&key={API_KEY}"
    response = requests.get(url).json()
    if response['status'] == 'OK':
        location = response['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"No se encontró ubicación para: {nombre_lugar}")
        return None

el_cafecito_coords = obtener_coordenadas("El Cafecito Zicatela, Puerto Escondido, México")
cafe_dans_coords = obtener_coordenadas("Café Dans, Puerto Escondido, México")

print("El Cafecito:", el_cafecito_coords)
print("Café Dans:", cafe_dans_coords)