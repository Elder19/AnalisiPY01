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
        self.soluciones = []
        
        # Validar puntos de inicio/fin
        if not (0 <= fila_inicio < self.filas and 0 <= col_inicio < self.columnas and
                0 <= fila_final < self.filas and 0 <= col_final < self.columnas):
            return False
            
        if self.datos[fila_inicio][col_inicio] == 0 or self.datos[fila_final][col_final] == 0:
            return False

        def backtrack(fila, col, camino, visitado):
            if (fila, col) in visitado:
                return
                
            camino.append((fila, col))
            visitado.add((fila, col))
            
            if [fila, col] == [fila_final, col_final]:
                self.soluciones.append(camino.copy())
            else:
                # Movimientos posibles (arriba, abajo, izquierda, derecha)
                for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    ni, nj = fila + di, col + dj
                    if 0 <= ni < self.filas and 0 <= nj < self.columnas:
                        if self.datos[ni][nj] == 1:
                            backtrack(ni, nj, camino, visitado)
            
            camino.pop()
            visitado.remove((fila, col))

        backtrack(fila_inicio, col_inicio, [], set())
        
        if self.soluciones:
            self.mejor_camino, self.peor_camino = self.seleccionSolucion(self.soluciones)
            return True
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
      
"""                      
"falta validar puntos de partida y final validos, guardar matriz y mostrar los 3 casos: peor, mejor y promedio"
m.CargarMatriz()
print("Original:")
print(m.mostrar())
m.menuPartida()
m.guardarMatriz()
"""
