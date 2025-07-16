import osmnx as ox
import networkx as nx
import folium
import math

from geopy.geocoders import Nominatim

# Crear geolocalizador
geolocator = Nominatim(user_agent="mi_app_de_rutas")

def calcularDistancia(puntoA, puntoB):
    print(puntoA["nombre"])
    print(puntoA["coordenadas"])
    print(puntoB["nombre"])
    print(puntoB["coordenadas"])
    return

# Buscar ubicación de El Cafecito
location_cafecito = geolocator.geocode("El Cafecito, Puerto Escondido, México")
print("El Cafecito:", (location_cafecito.latitude, location_cafecito.longitude))

# Buscar ubicación de Café Dans
nombres_cafe_dans = [
    "Dans Café Deluxe, Puerto Escondido, México",
    "Dan's Café Deluxe, Puerto Escondido, México",
    "Café Dans Zicatela, Puerto Escondido, México"
]

for nombre in nombres_cafe_dans:
    location_cafe_dans = geolocator.geocode(nombre)
    if location_cafe_dans :
        print(f"{nombre}: {(location_cafe_dans.latitude, location_cafe_dans.longitude)}")
        break
else:
    print("No se encontró Café Dans")

# Coordenadas de los lugares
el_cafecito = (location_cafecito.latitude, location_cafecito.longitude)
cafe_dans = (location_cafe_dans.latitude, location_cafe_dans.longitude)


cafe_dans = (15.850651714274541, -97.05272343237831)


# Crear grafo con buena cobertura
punto_central = ((el_cafecito[0] + cafe_dans[0]) / 2, (el_cafecito[1] + cafe_dans[1]) / 2)
G = ox.graph_from_point(punto_central, dist=1500, network_type='walk')

# Encontrar nodos más cercanos
origen = ox.distance.nearest_nodes(G, X=el_cafecito[1], Y=el_cafecito[0])
destino = ox.distance.nearest_nodes(G, X=cafe_dans[1], Y=cafe_dans[0])

# Calcular ruta más corta
ruta = nx.shortest_path(G, origen, destino, weight='length')

# Extraer coordenadas de la ruta
coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in ruta]

# Función para detectar giros
def calcular_angulo(p1, p2, p3):
    a = (p1[0] - p2[0], p1[1] - p2[1])
    b = (p3[0] - p2[0], p3[1] - p2[1])
    dot = a[0]*b[0] + a[1]*b[1]
    mag_a = math.hypot(*a)
    mag_b = math.hypot(*b)
    if mag_a * mag_b == 0:
        return 0
    cos_theta = dot / (mag_a * mag_b)
    ang = math.acos(max(min(cos_theta, 1), -1))
    return math.degrees(ang)

# Crear mapa centrado
m = folium.Map(location=punto_central, zoom_start=17)

# Dibujar ruta
folium.PolyLine(coords, color="blue", weight=5, opacity=0.7).add_to(m)

# Marcar puntos de inicio y fin
folium.Marker(coords[0], tooltip="El Cafecito", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(coords[-1], tooltip="Café Dans", icon=folium.Icon(color="red")).add_to(m)

folium.Marker(
    location=el_cafecito,
    tooltip="Ubicación original: El Cafecito",
    icon=folium.Icon(color="black", icon="circle")
).add_to(m)

folium.Marker(
    location=cafe_dans,
    tooltip="Ubicación original: Café Dans",
    icon=folium.Icon(color="black", icon="circle")
).add_to(m)

# Marcar los giros
for i in range(1, len(coords)-1):
    angulo = calcular_angulo(coords[i-1], coords[i], coords[i+1])
    if angulo < 150:
        folium.Marker(
            coords[i],
            icon=folium.Icon(icon="refresh", color="orange"),
            tooltip=f"Giro (ángulo {round(angulo,1)}°)"
        ).add_to(m)

# Guardar el mapa en archivo HTML
m.save("ruta_puerto_escondido.html")
print("✅ Mapa generado: abre el archivo 'ruta_puerto_escondido.html'")