import random, time
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
    """Escoje un numero ramdom
    Args:
    Returns:
        int: a ramdom number between 0 and 1.
    Raises:
    """
    def numero(self):
        return random.randint(0, 1)
    
    
    """create a matrix with walls and paths
    Args:
        filas (int): number of rows
        columnas (int): number of columns
    Returns:
        List[List[int]]: a matrix with walls (0) and paths (1).
    Raises:
    """
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
        """make new street 
        Args:
        Returns:
           List[List[int]]: a matrix with walls (0) and paths (1).
        Raises:
        """
        def sumaCaminos():
            for x in range(filas*columnas//10):
                x,y=random.randint(1,filas-1), random.randint(1,columnas-1)
                if grid[x][y]==0: 
                    grid[x][y]=1 #abre posibilidad 
                    #dfs(x,y)
        sumaCaminos()
        return grid
    
    """ Resolves the maze using dfs 
        Args:
            posicionO (tuple): starting position (row, column).
            posFinalO (tuple): ending position (row, column).
        Returns:
           
        Raises:
            false if the positions are ivalid or exceeds margin matrix  
        """
    def solucionarMatriz(self, posicionO, posFinalO):
        fila_inicio, col_inicio = posicionO
        fila_final, col_final = posFinalO
        todos_los_caminos = []
        Time=30
        Inicio=time.time()
        if not (0 <= fila_inicio < self.filas and 0 <= col_inicio < self.columnas and
            0 <= fila_final < self.filas and 0 <= col_final < self.columnas):
            
            return False
      
        if self.datos[fila_inicio][col_inicio] != 1 or self.datos[fila_final][col_final] != 1:
         
            return False
     
        """ Resolves the maze using dfs 
        Args:
            fila_inicio (int): starting row.
            col_inicio (int): starting column.
            camino (List[Tuple[int, int]]): current path.
            visitado (Set[Tuple[int, int]]): visited positions.

        Returns:
           true if a solution is found, false otherwise.
        Raises:
            false if the positions are ivalid or exceeds margin matrix  
        """
        def solucionarMatriz2(fila_inicio ,col_inicio,camino,visitado):
            if len(todos_los_caminos) >=20:
                return
            fila, columna = fila_inicio, col_inicio
            if time.time()-Inicio  > Time:
                return

            if (fila, columna) in visitado:
                return  
            camino.append((fila, columna))
            visitado.add((fila, columna))
            if [fila, columna] == [fila_final, col_final]:
                todos_los_caminos.append(camino.copy())
            else:
                if columna + 1 < self.columnas and self.datos[fila][columna + 1] == 1 :
                     solucionarMatriz2(fila,columna+1, camino, visitado)
                if columna - 1 >= 0 and self.datos[fila][columna - 1] == 1 :
                     solucionarMatriz2(fila,columna-1, camino, visitado)    
                if fila + 1 < self.filas and self.datos[fila + 1][columna] == 1   :
                     solucionarMatriz2(fila+1,columna, camino, visitado)
                if fila - 1 >= 0 and self.datos[fila - 1][columna] == 1 :
                    solucionarMatriz2(fila-1,columna, camino, visitado)

            camino.pop()
            visitado.remove((fila, columna))
        solucionarMatriz2(fila_inicio, col_inicio, [], set())
        if  len (todos_los_caminos)>0: 
                self.soluciones = todos_los_caminos
                self.soluciones.sort(key=len)
                return True
        else:
                
                return False
    
    """ save the matriz in a json file 
        Args: datos  data to save.
        Returns:
           returns true if the matriz is save else false
        Raises:
            false if the positions are ivalid or exceeds margin matrix  
        """
    def guardarMatriz(self):
        EXISTENTES = jm.cargarDatos()

        datos = {
            "filas": self.filas,
            "columnas": self.columnas,
            "matriz": self.matrizO
        }
        
        for matriz in EXISTENTES:
            if isinstance(matriz, dict) and matriz.get("matriz") == datos["matriz"]:
           
                return False  # Ya existe

        EXISTENTES.append(datos)
        jm.escribirMatriz(EXISTENTES)
        return True
    """ Reed the matrix of json file 
        Args:
            
        Returns:
          true is the matrix is reed else false 
        Raises:
            
        """
    def CargarMatriz(self,datos):
        """Carga una matriz desde JSON"""
        if datos and "matriz" in datos:
            self.matrizO = datos["matriz"]
            self.datos = [fila.copy() for fila in self.matrizO]
            self.filas = datos.get("filas", len(self.matrizO))
            self.columnas = datos.get("columnas", len(self.matrizO[0]) if self.filas > 0 else 0)
            return True
        return False
    """ Reseth the matrix to original  state
        Args:
        
        Returns:
           
        Raises:
           
        """
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

