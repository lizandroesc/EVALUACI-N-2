# Evaluacion2

Proyecto de la Evaluación Parcial N° 2 de la asignatura Telepresencia y Entornos Innovadores de Colaboración Humana (CUY6142), desarrollado en la máquina virtual DEVASC.

Contiene dos scripts de Python:

| Archivo | Descripción |
| --- | --- |
| `Ramdom50libros.py` | Agrega 50 libros con datos aleatorios (título, autor e ISBN) al catálogo de la API REST de la biblioteca y luego lista todos los libros. |
| `graphhopper_es.py` | Software de geolocalización con la API de GraphHopper: calcula rutas entre dos ubicaciones, con textos en español, valores numéricos con máximo dos decimales, narrativa del viaje en español y opción de salida con `s` o `salir`. |

## Requisitos

- Máquina virtual DEVASC (o un equipo con acceso a `http://library.demo.local`)
- Python 3
- Librería `requests`:

```bash
pip install requests
```

## Cómo ejecutar `Ramdom50libros.py`

1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:

```bash
python3 Ramdom50libros.py
```

El script inicia sesión en la API, crea los libros con ids del 8 al 57 y muestra el listado completo. Los ids 5, 6 y 7 corresponden a los libros agregados previamente con Postman, por lo que si el script ya se ejecutó, los ids pueden estar duplicados.

## Cómo ejecutar `graphhopper_es.py`

1. Contar con una clave API de GraphHopper (https://www.graphhopper.com).
2. Opcionalmente, guardarla en una variable de entorno para que el script no la pida:

```bash
export GRAPHHOPPER_KEY="su_clave_aqui"
```

3. Ejecutar:

```bash
python3 graphhopper_es.py
```

4. Ingresar el perfil de vehículo (`auto`, `bicicleta` o `a pie`), la ubicación de origen y el destino. El programa muestra la distancia, la duración y la narrativa del viaje.
5. Para terminar, escribir `s` o `salir` en cualquiera de las solicitudes.

La clave API no se guarda en el código del repositorio.
