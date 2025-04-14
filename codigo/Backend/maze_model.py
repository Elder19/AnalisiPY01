from typing import Tuple, List
import string
from enum import Enum, auto
import random

class CellType(Enum):
    EMPTY = auto()
    WALL = auto()
    START = auto()
    END = auto()
    VISITED = auto()
    SOLUTION = auto()
    CURRENT = auto()

class Maze:
    def __init__(self, size: int = 5):
        """
        Crea un laberinto cuadrado con:
        - Coordenadas tipo ajedrez (ej: a1, b3)
        - Punto de inicio definido por usuario (en borde)
        - Punto final:
          * En esquina opuesta si inicio está en esquina
          * En cualquier otro borde si inicio está en borde no esquina
        """
        if not 5 <= size <= 25:
            raise ValueError("El tamaño debe estar entre 5x5 y 25x25")
            
        self.size = size
        self.column_labels = string.ascii_lowercase[:size]
        self.row_labels = list(range(1, size+1))
        
        # Matriz interna
        self._grid = [[CellType.EMPTY for _ in range(size)] for _ in range(size)]
        
        # Inicialmente sin inicio/fin
        self._start = None
        self._end = None
        self.solution_path = []
        self.current_pos = None

    def set_start_point(self, col: str, row: int) -> None:
        """
        Establece el punto de inicio y automáticamente coloca el punto final:
        - En esquina opuesta si inicio está en esquina
        - En cualquier otro borde si inicio está en borde no esquina
        """
        x, y = self.convert_coords(col, row)
        
        # Validar que está en el borde
        if not self.is_border_cell(col, row):
            raise ValueError("El punto de inicio debe estar en el borde del laberinto")
            
        # Limpiar inicio anterior si existe
        if self._start:
            old_x, old_y = self._start
            self._grid[old_x][old_y] = CellType.EMPTY
        
        # Establecer nuevo inicio
        self._start = (x, y)
        self._grid[x][y] = CellType.START
        
        # Generar punto final según reglas especificadas
        self._generate_smart_end(x, y)

    def _generate_smart_end(self, start_x: int, start_y: int) -> None:
        """Genera punto final según las reglas especificadas"""
        # Limpiar fin anterior si existe
        if self._end:
            old_x, old_y = self._end
            self._grid[old_x][old_y] = CellType.EMPTY
        
        # Mapeo de esquinas opuestas
        corner_mapping = {
            (0, 0): (self.size-1, self.size-1),  # NW → SE
            (0, self.size-1): (self.size-1, 0),   # SW → NE
            (self.size-1, 0): (0, self.size-1),   # NE → SW
            (self.size-1, self.size-1): (0, 0)     # SE → NW
        }
        
        # Caso 1: Inicio en esquina → Fin en esquina opuesta
        if (start_x, start_y) in corner_mapping:
            end_x, end_y = corner_mapping[(start_x, start_y)]
        # Caso 2: Inicio en borde no esquina → Fin en cualquier otro borde
        else:
            border_cells = []
            
            # Borde superior (excluyendo esquinas)
            if start_y != 0:
                border_cells.extend([(x, 0) for x in range(self.size)])
            
            # Borde inferior (excluyendo esquinas)
            if start_y != self.size-1:
                border_cells.extend([(x, self.size-1) for x in range(self.size)])
            
            # Borde izquierdo (excluyendo esquinas)
            if start_x != 0:
                border_cells.extend([(0, y) for y in range(1, self.size-1)])
            
            # Borde derecho (excluyendo esquinas)
            if start_x != self.size-1:
                border_cells.extend([(self.size-1, y) for y in range(1, self.size-1)])
            
            # Eliminar la celda de inicio y adyacentes inmediatos
            border_cells = [
                (x, y) for (x, y) in border_cells 
                if not (x == start_x and y == start_y)
                and abs(x - start_x) + abs(y - start_y) > 1
            ]
            
            if not border_cells:
                raise ValueError("No se pudo generar posición final válida")
            
            end_x, end_y = random.choice(border_cells)
        
        # Establecer punto final
        self._end = (end_x, end_y)
        self._grid[end_x][end_y] = CellType.END

    def convert_coords(self, col: str, row: int) -> Tuple[int, int]:
        """Convierte coordenadas tipo ajedrez a índices internos"""
        col = col.lower()
        if (col not in self.column_labels or 
            not 1 <= row <= self.size):
            raise ValueError(f"Coordenadas inválidas. Rango: {self.column_labels[0]}-{self.column_labels[-1]} y 1-{self.size}")
        return self.column_labels.index(col), row - 1

    def is_border_cell(self, col: str, row: int) -> bool:
        """Verifica si una celda está en el borde"""
        x, y = self.convert_coords(col, row)
        return (x == 0 or x == self.size-1 or y == 0 or y == self.size-1)

    def is_corner_cell(self, col: str, row: int) -> bool:
        """Verifica si una celda está en una esquina"""
        x, y = self.convert_coords(col, row)
        return (x, y) in [
            (0, 0), 
            (0, self.size-1), 
            (self.size-1, 0), 
            (self.size-1, self.size-1)
        ]

    def __str__(self):
        """Representación visual con coordenadas"""
        header = "   " + " ".join(self.column_labels.upper()) + "\n"
        rows = []
        
        for y in range(self.size):
            row_label = f"{self.row_labels[y]:2} "
            cells = []
            
            for x in range(self.size):
                cell = self._grid[x][y]
                symbol = {
                    CellType.EMPTY: '·',
                    CellType.WALL: '█',
                    CellType.START: 'S',
                    CellType.END: 'E',
                    CellType.VISITED: '.',
                    CellType.SOLUTION: '★',
                    CellType.CURRENT: '○'
                }[cell]
                cells.append(symbol)
            
            rows.append(row_label + " ".join(cells))
        
        return header + "\n".join(rows)