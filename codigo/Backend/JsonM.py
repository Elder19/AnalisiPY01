import json
""" charge the matrix in the and save the matrix in the json file
        Args:
        Returns:
           return datos in a list
        Raises:
            execpt if  FileNotFoundError,JSONDecodeError
        """
def cargarDatos():
    try:
        with open('datos.json', 'r') as archivo:
            datos = json.load(archivo)
            if isinstance(datos, dict):
                datos = [datos]
            return datos
    except (FileNotFoundError, json.JSONDecodeError):
        return []
""" write the matrix in the json file
        Args:
            lista_matrices: list of matrix to save in the json 
        Returns:
           return true if the matrix is saved
        Raises:
        """
def escribirMatriz(lista_matrices):
    with open('datos.json', 'w') as archivo:
        json.dump(lista_matrices, archivo, indent=6)
    return True
