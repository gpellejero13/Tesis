import csv
import re
import folium

# Ruta al archivo CSV
archivo = 'RedRefill.csv'

# Diccionario para guardar los cafés por nombre
RedRefill = {}

# Función para extraer coordenadas del campo WKT
def extraer_coordenadas(wkt):
    match = re.search(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)', wkt)
    if match:
        lon = float(match.group(1))
        lat = float(match.group(2))
        return (lon, lat)
    return None

# Leer el archivo CSV
with open(archivo, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nombre = row['Nombre'].strip()
        coordenadas = extraer_coordenadas(row['WKT'])
        if nombre and coordenadas:
            RedRefill[nombre] = {
                'nombre': nombre,
                'coordenadas': coordenadas,
                'descripcion': row['Descripción'].strip() if row['Descripción'] else ''
            }

# Centro del mapa (puedes ajustar según tus datos)
centro = [15.838, -97.046]

# Crear el mapa
mapa = folium.Map(location=centro, zoom_start=14, tiles="OpenStreetMap")

# Añadir la hoja de estilos de Font Awesome en el HTML del mapa
font_awesome_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'
mapa.get_root().html.add_child(folium.Element(font_awesome_css))

# Agregar los puntos con iconos
for lugar in RedRefill.values():
    print(lugar["nombre"])
    folium.Marker(
        location=lugar["coordenadas"],
        popup=lugar["nombre"],
        tooltip=lugar["nombre"],
        icon =folium.Icon(color="black", icon="circle")

    ).add_to(mapa)

# Guardar el mapa
mapa.save('redrefill_mapa.html')