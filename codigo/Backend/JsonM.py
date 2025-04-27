import json 

def cargarDatos():
    with open('datos.json','r') as arcvhivo: 
        datos= json.load(arcvhivo)
        return datos

import json

def escribirMatriz(Dmatriz):
    try:

        with open('datos.json', 'r') as archivo:
            try:
                datos = json.load(archivo)
               
                if isinstance(datos, dict):
                    datos = [datos]
            except json.JSONDecodeError:
                
                datos = []
    except FileNotFoundError:
    
        datos = []
 
    datos.append(Dmatriz)

    with open('datos.json', 'w') as archivo:
        json.dump(datos, archivo, indent=6) 
    return True
