import random
from PyQt5.QtWidgets import QMessageBox
class matriz: 

    def __init__(self, filas, columnas):
            self.filas = filas
            self.columnas = columnas
            self.datos = self.crearMatriz(filas, columnas)
            self.matrizO=self.crearMatriz(filas, columnas)
            self.soluciones=[]
            
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

        resultado = "    "+" ".join(f"{j:2}" for j in range(self.columnas)) + "\n"
        resultado += "   " + "---" * self.columnas + "\n"
        for i, fila in enumerate(self.datos):
            resultado += f"{i:2} | " + "  ".join(str(valor) for valor in fila) + "\n"
        return resultado

    def solucionarMatriz(self, posicionO, posFinalO):
        fila_inicio, col_inicio = posicionO
        fila_final, col_final = posFinalO
        todos_los_caminos = []

        def solucionarMatriz2(fila ,columna,camino,visitado):
            if (fila, columna) in visitado:
                return
            camino.append((fila, columna))
            visitado.add((fila, columna))
            if [fila, columna] == [fila_final, col_final]:
                todos_los_caminos.append(camino.copy())
            else:
                if fila + 1 < self.filas and self.datos[fila + 1][columna] == 1   :
                     solucionarMatriz2(fila+1,columna, camino, visitado)
                if fila - 1 >= 0 and self.datos[fila - 1][columna] == 1 :
                    solucionarMatriz2(fila-1,columna, camino, visitado)
                if columna + 1 < self.columnas and self.datos[fila][columna + 1] == 1 :
                     solucionarMatriz2(fila,columna+1, camino, visitado)
                if columna - 1 >= 0 and self.datos[fila][columna - 1] == 1 :
                     solucionarMatriz2(fila,columna-1, camino, visitado)
                
            camino.pop()
            visitado.remove((fila, columna))
        
        solucionarMatriz2(fila_inicio, col_inicio, [], set())
        for numero,camino in enumerate(todos_los_caminos):
            for fila, col in camino:
                print (numero)
                self.cambiarSigno(fila, col,numero+1)
        if  len (todos_los_caminos)>0: 
            self.seleccionSolucion(todos_los_caminos)       
            return self.mostrar()  
        else:
            print("no hay solucion en el punto de partida")       
                 
    def menuPartida(self):
        fila = int(input("Ingrese la fila de partida: "))
        columna = int(input("Ingrese la columna de partida: "))
        filaFinal = int(input("Ingrese la fila final: "))
        columnaFinal = int(input("Ingrese la columna final: "))
        if  self.datos[fila][columna] !=0 and self.datos[filaFinal][columnaFinal]!=0:
            print("\nDespués de solucionar:\n")
            print(self.solucionarMatriz([fila, columna], [filaFinal, columnaFinal]))
        else: 
            return False 
        
    def cambiarSigno(self, fila, columma,signo):
        if self.datos[fila][columma]==1:
            self.datos[fila][columma]=signo
        else: 
              self.datos[fila][columma]=3
        return (self.datos[fila][columma])
    
    def devolverSigno(self, fila, columma):
        self.datos[fila][columma]=1
            
        return (self.datos[fila][columma])                   
    def seleccionSolucion(self,caminos):
        mejorCaso=[]
        peorCaso=[]
        casoPromedio=[]
        
        for x in caminos:
            if len(x)<len(mejorCaso) or mejorCaso==[]:
                    mejorCaso=x
            elif  len(x)>len(peorCaso) or peorCaso==[]:
                    peorCaso=x
            #preguntar si es nesesario el caso promedio de pasos  
        print(mejorCaso)
        print(peorCaso)
    
                      
"falta validar puntos de partida y final validos, guardar matriz y mostrar los 3 caso peor mejor y promedio"
m = matriz(20, 20)
print("Original:")
print(m.mostrar())
m.menuPartida()
