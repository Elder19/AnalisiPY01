import json 

def cargarDatos():
    with open('datos.json','r') as arcvhivo: 
        datos= json.load(arcvhivo)
        return datos


def escribirMatriz(Dmatriz):
    with open('datos.json','w') as archivo: 
        json.dump(Dmatriz,archivo)
    return True
