import osmnx as ox
import networkx as nx

# Establece el lugar base
lugar = "Puerto Escondido, Oaxaca, Mexico"

el_cafecito = (15.852342497310238, -97.05437332409241)  # El Cafecito (Zicatela)
cafe_dans = (15.85076599630929, -97.05243089578931)    # Café Dans

# Usa el punto medio entre ambos lugares como referencia
punto_central = ((el_cafecito[0] + cafe_dans[0]) / 2, (el_cafecito[1] + cafe_dans[1]) / 2)

# Descargar la red de Puerto Escondido entre los puntos
print("Descargando red...")

# Construye un grafo peatonal amplio (1.5 km a la redonda)
G = ox.graph_from_point(punto_central, dist=1500, network_type='walk', simplify=True)

# Verifica nodos más cercanos nuevamente
origen = ox.distance.nearest_nodes(G, X=el_cafecito[1], Y=el_cafecito[0])
destino = ox.distance.nearest_nodes(G, X=cafe_dans[1], Y=cafe_dans[0])

# Calcular ruta más corta por carretera
ruta = nx.shortest_path(G, origen, destino, weight='length')

# Calcular distancia total en metros
distancia_m = 0
for u, v in zip(ruta[:-1], ruta[1:]):
    data = G.get_edge_data(u, v)
    # Algunos grafos tienen múltiples aristas entre nodos, elegimos la primera
    edge = data[0] if isinstance(data, dict) else data
    distancia_m += edge['length']
    print("Nodo...", edge['length'])

print(f"Distancia entre El Cafecito y Café Dans: {distancia_m:.2f} mts")

from geopy.distance import geodesic
print("Distancia en línea recta:", geodesic(el_cafecito, cafe_dans).meters, "m")

for i, node in enumerate(ruta):
    x = G.nodes[node]['x']  # longitud
    y = G.nodes[node]['y']  # latitud
    print(f"Punto {i+1}: ({y}, {x})")