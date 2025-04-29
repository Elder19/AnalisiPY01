import json

def cargarDatos():
    try:
        with open('datos.json', 'r') as archivo:
            datos = json.load(archivo)
            if isinstance(datos, dict):
                datos = [datos]
            return datos
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escribirMatriz(lista_matrices):
    with open('datos.json', 'w') as archivo:
        json.dump(lista_matrices, archivo, indent=6)
    return True
