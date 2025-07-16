import levantarArchivoDeLaRed
import distanciaCaminando
from datetime import datetime

redRefill = levantarArchivoDeLaRed.RedRefill

#distancia = distanciaCaminando.distancia_caminando("Hotel San Juan", "Café Botánico Pto. Escondido", redRefill, "resultado.html")

print(datetime.now(), " - Inician busquedas")
for lugar in redRefill.values():
    if lugar["nombre"] != "Aquatis Albercas y Spas":
        distancia = distanciaCaminando.distancia_caminando(lugar["nombre"], "Café Botánico Pto. Escondido", redRefill,
                                                       "resultado.html")
print(datetime.now(), " - Terminan busquedas")
