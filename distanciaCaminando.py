import osmnx as ox
import networkx as nx
from datetime import datetime

punto_central = (15.8577107, -97.05819620000001)

print(datetime.now(), " - Inicia lee mapa")
G = ox.graph_from_point(punto_central, dist=20000, network_type='walk', retain_all=True)
print(datetime.now(), " - Termina lee mapa")


def distancia_caminando(nombre1, nombre2, red, archivoRuta=""):
    if nombre1 not in red or nombre2 not in red:
        print("Uno o ambos lugares no se encontraron:", '{nombre1}', '{nombre2}')
        return f"Uno o ambos lugares no se encontraron: '{nombre1}', '{nombre2}'"

    lat1, lon1 = red[nombre1]['coordenadas'][1], red[nombre1]['coordenadas'][0]
    lat2, lon2 = red[nombre2]['coordenadas'][1], red[nombre2]['coordenadas'][0]

    # Buscar nodos más cercanos
    origen = ox.distance.nearest_nodes(G, lat1,lon1)
    destino = ox.distance.nearest_nodes(G, lat2,lon2)

    # Calcular la ruta más corta en metros
    try:
        ruta = nx.shortest_path(G, origen, destino, weight='length')
        distancia = sum(
            G[u][v][0]['length'] for u, v in zip(ruta[:-1], ruta[1:])
        )
        if archivoRuta != "":
            mostrar_ruta_en_mapa(G, ruta, nombre_archivo=archivoRuta)
        return distancia
    except Exception as e:
        return f"No se pudo calcular la ruta: {e}"


import folium
import osmnx as ox
import networkx as nx

def mostrar_ruta_en_mapa(G, ruta, nombre_archivo='ruta_mapa.html'):
    # Obtener coordenadas (lat, lon) de los nodos en la ruta
    coordenadas = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in ruta]

    # Centrar el mapa en el primer punto
    mapa = folium.Map(location=coordenadas[0], zoom_start=16)

    # Agregar la línea de la ruta
    folium.PolyLine(
        coordenadas,
        color='blue',
        weight=5,
        opacity=0.8,
        tooltip='Ruta caminando'
    ).add_to(mapa)

    # Agregar marcador de inicio
    folium.Marker(
        location=coordenadas[0],
        popup="Inicio",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(mapa)

    # Agregar marcador de fin
    folium.Marker(
        location=coordenadas[-1],
        popup="Destino",
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(mapa)

    # Guardar a archivo
    mapa.save(nombre_archivo)
