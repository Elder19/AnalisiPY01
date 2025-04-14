import random
from PyQt5.QtWidgets import QMessageBox
class matriz: 

    def __init__(self, filas, columnas):
            self.filas = filas
            self.columnas = columnas
            self.datos = self.crearMatriz(filas, columnas)
            self.matrizO=self.crearMatriz(filas, columnas)
            
    def numero(self):
            return random.randint(0, 1)

    def crearMatriz(self, filas, columnas):
        Matriz = []
        for i in range(filas):
            fila = []
            for n in range(columnas):
                fila.append(self.numero())
            Matriz.append(fila)
        return Matriz

    
    def mostrar(self):
        resultado = "    " + "  ".join(f"{j:2}" for j in range(self.columnas)) + "\n"
        resultado += "   " + "---" * self.columnas + "\n"
        for i, fila in enumerate(self.datos):
            resultado += f"{i:2} | " + "  ".join(str(valor) for valor in fila) + "\n"
        return resultado

    
    def solucionarMatriz(self,posicionO ,posFinalO):
        posicion=posicionO
        posFinal = posFinalO
        pospasada=[]
        camino=[]
        
        while posicion!= posFinal:
            fila, columna = posicion
            pospasada.append(posicion[:])
            camino.append(posicion[:])
            self.cambiarSigno(fila,columna)

             # Movimiento hacia abajo
            if fila + 1 < self.filas and self.datos[fila + 1][columna] == 1 and [fila + 1, columna] not in pospasada:
                posicion = [fila + 1, columna]
                
                continue

            # Movimiento hacia arriba
            elif fila - 1 >= 0 and self.datos[fila - 1][columna] == 1 and [fila - 1, columna] not in pospasada:
                posicion = [fila - 1, columna]
                continue

            # Movimiento hacia la derecha
            elif columna + 1 < self.columnas and self.datos[fila][columna + 1] == 1 and [fila, columna + 1] not in pospasada:
                posicion = [fila, columna + 1]
                continue

            # Movimiento hacia la izquierda
            elif columna - 1 >= 0 and self.datos[fila][columna - 1] == 1 and [fila, columna - 1] not in pospasada:
                posicion = [fila, columna - 1]
                continue

            # Si no hay camino posible
            break
                
        return self.mostrar()
        
    def menuPartida():
        fila=input("ingrese la fila de partida")
        columna=input("ingrese la columna de partida")
        filaFinal=input("ingrese la fila final")
        columnaFinal=input("ingrese la columna final")  
    def cambiarSigno(self, fila, columma):
        self.datos[fila][columma]=3
        return (self.datos[fila][columma])
    
    def devolverSigno(self, fila, columma):
        self.datos[fila][columma]=1
        return (self.datos[fila][columma])                   
                        

m = matriz(25, 15)
print("Original:")
print(m.mostrar())
print("\nDespués de solucionar:")
print(m.solucionarMatriz([1,1],[10,3]))