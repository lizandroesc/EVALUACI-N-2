import random
import requests
 
BASE_URL = "http://library.demo.local/api/v1"
USUARIO = "cisco"
CLAVE = "Cisco123!"
 
NOMBRES = ["Camila", "Mateo", "Valentina", "Benjamin", "Sofia", "Joaquin",
           "Isidora", "Vicente", "Antonia", "Tomas", "Martina", "Felipe"]
APELLIDOS = ["Gonzalez", "Munoz", "Rojas", "Diaz", "Perez", "Soto",
             "Contreras", "Silva", "Martinez", "Sepulveda", "Morales", "Fuentes"]
PALABRAS_1 = ["Introduccion a", "Fundamentos de", "Manual de", "Guia de",
              "Secretos de", "Taller de", "Historia de", "Principios de"]
PALABRAS_2 = ["las Redes", "la Programacion", "la Automatizacion", "las APIs",
              "la Ciberseguridad", "los Datos", "la Nube", "Python"]
 
 
def obtener_clave():
    """Hace login con Basic Auth y devuelve la clave de la API."""
    r = requests.post(f"{BASE_URL}/loginViaBasic", auth=(USUARIO, CLAVE))
    r.raise_for_status()
    datos = r.json()
    for campo in ("token", "api_key", "apiKey", "key", "X-API-KEY"):
        if campo in datos:
            return datos[campo]
    raise SystemExit(f"No encontre la clave en la respuesta: {datos}")
 
 
def libro_al_azar(id_libro):
    return {
        "id": id_libro,
        "title": f"{random.choice(PALABRAS_1)} {random.choice(PALABRAS_2)}",
        "author": f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
        "isbn": "".join(random.choices("0123456789", k=10)),
    }
 
 
def main():
    clave = obtener_clave()
    headers = {"X-API-KEY": clave, "Content-Type": "application/json"}
 
    # Los ids 5, 6 y 7 ya existen, se parte desde el 8
    for id_libro in range(8, 58):
        libro = libro_al_azar(id_libro)
        r = requests.post(f"{BASE_URL}/books", json=libro, headers=headers)
        print(f"Libro {id_libro}: {r.status_code} - {libro['title']} / {libro['author']}")
 
    print("\n--- Listado completo de libros ---")
    r = requests.get(f"{BASE_URL}/books", headers={"X-API-KEY": clave})
    print(f"Estado: {r.status_code}")
    if r.status_code == 200:
        for libro in r.json():
            print(libro)
    else:
        print(r.text)
 
 
if __name__ == "__main__":
    main()