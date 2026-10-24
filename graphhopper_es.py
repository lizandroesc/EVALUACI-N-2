import os
import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = os.environ.get("GRAPHHOPPER_KEY") or input("Ingrese su clave API de Graphhopper: ")

perfiles = {"auto": "car", "bicicleta": "bike", "a pie": "foot"}


def es_salida(texto):
    return texto.strip().lower() in ("s", "salir")


def geocodificar(ubicacion, key):
    url = "https://graphhopper.com/api/1/geocode?" + urllib.parse.urlencode(
        {"q": ubicacion, "limit": "1", "key": key}
    )
    respuesta = requests.get(url)
    estado = respuesta.status_code
    datos = respuesta.json()
    if estado == 200 and len(datos.get("hits", [])) > 0:
        hit = datos["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        nombre = hit.get("name", "")
        estado_region = hit.get("state", "")
        pais = hit.get("country", "")
        nueva_ubicacion = ", ".join(x for x in (nombre, estado_region, pais) if x)
        print(f"URL de la API de geocodificación para {nueva_ubicacion}:\n{url}")
        return estado, lat, lng, nueva_ubicacion
    print(f"No se pudo geocodificar '{ubicacion}'. Código de estado: {estado}")
    return estado, None, None, ubicacion


while True:
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("auto, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    perfil = input("Ingrese un perfil de la lista (o 's' / 'salir' para terminar): ")
    if es_salida(perfil):
        print("Programa finalizado. ¡Hasta luego!")
        break
    vehiculo = perfiles.get(perfil.strip().lower())
    if vehiculo is None:
        vehiculo = "car"
        print("Perfil no válido. Se usará el perfil 'auto'.")

    origen_txt = input("Ubicación de origen (o 's' / 'salir'): ")
    if es_salida(origen_txt):
        print("Programa finalizado. ¡Hasta luego!")
        break
    destino_txt = input("Destino (o 's' / 'salir'): ")
    if es_salida(destino_txt):
        print("Programa finalizado. ¡Hasta luego!")
        break

    orig = geocodificar(origen_txt, key)
    dest = geocodificar(destino_txt, key)

    if orig[0] == 200 and dest[0] == 200 and orig[1] is not None and dest[1] is not None:
        puntos = f"&point={orig[1]}%2C{orig[2]}&point={dest[1]}%2C{dest[2]}"
        url_ruta = route_url + urllib.parse.urlencode(
            {"key": key, "vehicle": vehiculo, "locale": "es"}
        ) + puntos
        resp = requests.get(url_ruta)
        datos = resp.json()
        print("=================================================")
        print(f"Estado de la API de rutas: {resp.status_code}")
        print(f"URL de la API de rutas:\n{url_ruta}")
        print("=================================================")
        if resp.status_code == 200:
            camino = datos["paths"][0]
            km = camino["distance"] / 1000
            millas = km / 1.61
            total_seg = int(camino["time"] / 1000)
            horas, resto = divmod(total_seg, 3600)
            minutos, segundos = divmod(resto, 60)
            print(f"Direcciones desde {orig[3]} hasta {dest[3]} en {perfil.strip().lower()}")
            print("=================================================")
            print(f"Distancia recorrida: {millas:.2f} millas / {km:.2f} km")
            print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")
            print("=================================================")
            for paso in camino["instructions"]:
                d_km = paso["distance"] / 1000
                print(f"{paso['text']} ( {d_km:.2f} km / {d_km / 1.61:.2f} millas )")
            print("=================================================")
        else:
            print("Mensaje de error:", datos.get("message", "sin detalle"))
    else:
        print("No se pudo calcular la ruta. Revise las ubicaciones ingresadas.")