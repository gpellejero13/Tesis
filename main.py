# import levantarArchivoDeLaRed
# import distanciaCaminando
# from datetime import datetime
import generaMapaDesdeCSV

# Asegúrate de que este nombre de archivo coincida con el CSV que generaste
# Por ejemplo, si usaste el script de la cuadrícula específica, sería:
csv_input_file = "comercios_puerto_escondido_cuadro_especifico.csv"

# Puedes ajustar el centro del mapa si prefieres un punto diferente
# o incluso calcularlo dinámicamente a partir de los datos del CSV
generaMapaDesdeCSV.generate_html_map_from_csv(csv_input_file,
                           map_center_lat=15.8748, # Latitud más al centro del área que definiste
                           map_center_lon=-97.0814, # Longitud más al centro del área que definiste
                           initial_zoom=14)

print("\nPara ver el mapa, abre el archivo HTML generado en tu navegador web.")

# redRefill = levantarArchivoDeLaRed.RedRefill
#
# distancia = distanciaCaminando.distancia_caminando("Hotel San Juan", "Café Botánico Pto. Escondido", redRefill, "resultado.html")
#
# print(datetime.now(), " - Inician busquedas")
# for lugar in redRefill.values():
#     if lugar["nombre"] != "Aquatis Albercas y Spas":
#         distancia = distanciaCaminando.distancia_caminando(lugar["nombre"], "Café Botánico Pto. Escondido", redRefill,
#                                                        "resultado.html")
# print(datetime.now(), " - Terminan busquedas")
