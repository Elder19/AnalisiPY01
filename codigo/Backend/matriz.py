import random
from Backend import JsonM as jm
from PySide6.QtWidgets import QMessageBox

class matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = self.crearMatriz(filas, columnas)
        self.matrizO = [fila.copy() for fila in self.datos]  # Copia original
        self.soluciones = []
        self.mejor_camino = None
        self.peor_camino = None

    def numero(self):
        return random.randint(0, 1)

    def crearMatriz(self, filas, columnas):
        # Inicializar todo como paredes (0)
        grid = [[0 for _ in range(columnas)] for _ in range(filas)]
  
        def dfs(x, y):
            direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(direcciones)
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if 0 <= nx < filas and 0 <= ny < columnas and grid[nx][ny] == 0:
                    # Cavar camino
                    grid[x + dx//2][y + dy//2] = 1
                    grid[nx][ny] = 1
                    dfs(nx, ny)

        # Punto inicial
        start_x, start_y = 0, 0
        grid[start_x][start_y] = 1
        dfs(start_x, start_y)
        def sumaCaminos():
            for x in range(filas*columnas//5):
                x,y=random.randint(1,filas-1), random.randint(1,columnas-1)
                if grid[x][y]==0: 
                    grid[x][y]=1 #abre posibilidad 
                    #dfs(x,y)
        sumaCaminos()
        return grid
    
    
    def mostrar(self):
        resultado = "    " + " ".join(f"{j:2}" for j in range(self.columnas)) + "\n"
        resultado += "   " + "---" * self.columnas + "\n"
        for i, fila in enumerate(self.datos):
            resultado += f"{i:2} | " + "  ".join(str(valor) for valor in fila) + "\n"
        return resultado

    def solucionarMatriz(self, posicionO, posFinalO):
        fila_inicio, col_inicio = posicionO
        fila_final, col_final = posFinalO
        todos_los_caminos = []
     
        if not (0 <= fila_inicio < self.filas and 0 <= col_inicio < self.columnas and
            0 <= fila_final < self.filas and 0 <= col_final < self.columnas):
            print("Puntos de inicio o fin están fuera de los límites.")
            return False
      
        if self.datos[fila_inicio][col_inicio] != 1 or self.datos[fila_final][col_final] != 1:
            print("Puntos de inicio o fin no son transitables.")
            return False
     
        
        def solucionarMatriz2(fila_inicio ,col_inicio,camino,visitado):
            if len(todos_los_caminos) >= 3:
                return
            fila, columna = fila_inicio, col_inicio
            print("solucionando matriz 3")
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
        if  len (todos_los_caminos)>0: 
                self.mejor_camino, self.peor_camino = self.seleccionSolucion(todos_los_caminos)
                self.soluciones = todos_los_caminos
                return True
        else:
                print("no hay solucion en el punto de partida") 
                return False
      
    def cambiarSigno(self, fila, columna, signo):
        #Marca celdas del camino con números (2 para mejor, 3 para peor, etc.)
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.datos[fila][columna] = signo
        return self.datos[fila][columna]

    def devolverSigno(self, fila, columna):
        """Restaura una celda a su valor original (1)"""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.datos[fila][columna] = 1
        return self.datos[fila][columna]

    def seleccionSolucion(self, caminos):
        """Identifica el mejor y peor camino"""
        if not caminos:
            return None, None
        mejor = min(caminos, key=len)
        peor = max(caminos, key=len)
        return mejor, peor

    def guardarMatriz(self, nombre="laberinto_guardado"):
        """Guarda la matriz original en JSON"""
        datos = {
            "filas": self.filas,
            "columnas": self.columnas,
            "matriz": self.matrizO
        }
        jm.escribirMatriz(datos)
        return True

    def CargarMatriz(self):
        """Carga una matriz desde JSON"""
        datos = jm.cargarDatos()
        if datos and "matriz" in datos:
            self.matrizO = datos["matriz"]
            self.datos = [fila.copy() for fila in self.matrizO]
            self.filas = datos.get("filas", len(self.matrizO))
            self.columnas = datos.get("columnas", len(self.matrizO[0]) if self.filas > 0 else 0)
            return True
        return False

    def resetearMatriz(self):
        """Restaura la matriz a su estado original"""
        self.datos = [fila.copy() for fila in self.matrizO]
        self.soluciones = []
        self.mejor_camino = None
        self.peor_camino = None
    def puntoFInal(self):
        "escoje al azar un punto final"
        x,y=random.randint(1,self.filas-1), random.randint(1,self.columnas-1)
        if self.datos[x][y]==1: 
            return x,y
        return self.puntoFInal()
"""                      
"falta validar puntos de partida y final validos, guardar matriz y mostrar los 3 casos: peor, mejor y promedio"
m.CargarMatriz()
print("Original:")
print(m.mostrar())
m.menuPartida()
m.guardarMatriz()
"""
