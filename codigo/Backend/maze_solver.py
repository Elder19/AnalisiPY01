from typing import List, Tuple, Optional
from .maze_model import Maze, CellType

class MazeSolver:
    @staticmethod
    def solve(maze: Maze, allow_diagonal: bool = False) -> bool:
        """
        Resuelve el laberinto usando backtracking y muestra el camino.
        
        Args:
            maze: Instancia del laberinto a resolver
            allow_diagonal: Si permite movimientos diagonales (opcional)
            
        Returns:
            True si encontró solución, False si no
        """
        # Limpiar soluciones previas
        maze.solution_path = []
        
        # Direcciones de movimiento
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Movimientos ortogonales
        if allow_diagonal:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # + diagonales

        # Función recursiva de backtracking
        def backtrack(x: int, y: int) -> bool:
            # Verificar si llegamos al final
            if (x, y) == maze._end:
                maze.solution_path.append((x, y))
                return True
                
            # Marcar celda como visitada
            if (x, y) != maze._start:
                original_type = maze._grid[x][y]
                maze._grid[x][y] = CellType.VISITED
            
            # Intentar todos los movimientos posibles
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < maze.size and 0 <= ny < maze.size and
                    maze._grid[nx][ny] not in (CellType.WALL, CellType.VISITED)):
                    
                    if backtrack(nx, ny):
                        maze.solution_path.append((x, y))
                        # Marcar como parte de la solución (excepto inicio/fin)
                        if (x, y) not in (maze._start, maze._end):
                            maze._grid[x][y] = CellType.SOLUTION
                        return True
            
            # Backtrack si no se encontró solución
            if (x, y) != maze._start:
                maze._grid[x][y] = original_type
            return False

        # Iniciar búsqueda desde el punto de inicio
        start_x, start_y = maze._start
        return backtrack(start_x, start_y)

    @staticmethod
    def has_solution(maze: Maze) -> bool:
        """Versión optimizada solo para verificar existencia de solución"""
        visited = set()
        
        def can_reach(x: int, y: int) -> bool:
            if (x, y) == maze._end:
                return True
                
            if (x, y) in visited or not (0 <= x < maze.size and 0 <= y < maze.size):
                return False
                
            if maze._grid[x][y] in (CellType.WALL, CellType.VISITED):
                return False
                
            visited.add((x, y))
            
            # Prueba movimientos ortogonales primero (más eficiente)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if can_reach(x + dx, y + dy):
                    return True
                    
            return False

        return can_reach(*maze._start)

    @staticmethod
    def find_path(maze: Maze) -> Optional[List[Tuple[int, int]]]:
        """Devuelve el camino solución como lista de coordenadas"""
        if MazeSolver.solve(maze):
            return maze.solution_path[::-1]  # Invertir para que vaya de inicio a fin
        return None
    