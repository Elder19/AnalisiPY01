import random
from typing import List, Tuple, Set
from .maze_model import Maze, CellType

class MazeGenerator:
    @staticmethod
    def generate_perfect_maze(maze: Maze) -> Maze:
        """
        Genera un laberinto 'perfecto' (con exactamente un camino entre cualquier par de celdas)
        usando el algoritmo de Prim.
        """
        size = maze.size
        start_x, start_y = maze._start
        end_x, end_y = maze._end

        # Inicializar todo como paredes
        maze._grid = [[CellType.WALL for _ in range(size)] for _ in range(size)]
        
        # Asegurar que inicio y fin son caminos
        maze._grid[start_x][start_y] = CellType.START
        maze._grid[end_x][end_y] = CellType.END

        # Celda inicial para comenzar la generación (aleatoria)
        init_x, init_y = random.randint(1, size-2), random.randint(1, size-2)
        maze._grid[init_x][init_y] = CellType.EMPTY

        # Lista de paredes adyacentes a celdas visitadas
        walls = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = init_x + dx, init_y + dy
            if 0 < nx < size-1 and 0 < ny < size-1:
                walls.append((nx, ny, init_x, init_y))

        while walls:
            # Elegir una pared aleatoria
            wall_x, wall_y, parent_x, parent_y = random.choice(walls)
            walls.remove((wall_x, wall_y, parent_x, parent_y))

            # Verificar si al convertirlo en camino conecta áreas no conectadas
            opposite_x, opposite_y = 2*wall_x - parent_x, 2*wall_y - parent_y
            
            if 0 < opposite_x < size-1 and 0 < opposite_y < size-1:
                if maze._grid[opposite_x][opposite_y] == CellType.WALL:
                    # Convertir pared y celda opuesta en camino
                    maze._grid[wall_x][wall_y] = CellType.EMPTY
                    maze._grid[opposite_x][opposite_y] = CellType.EMPTY

                    # Añadir nuevas paredes a la lista
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = opposite_x + dx, opposite_y + dy
                        if 0 < nx < size-1 and 0 < ny < size-1 and maze._grid[nx][ny] == CellType.WALL:
                            walls.append((nx, ny, opposite_x, opposite_y))

        return maze

    @staticmethod
    def generate_with_backtracking(maze: Maze) -> Maze:
        """
        Genera un laberinto usando el algoritmo de backtracking recursivo.
        Produce laberintos con muchos caminos muertos.
        """
        size = maze.size
        start_x, start_y = maze._start
        end_x, end_y = maze._end

        # Inicializar todo como paredes
        maze._grid = [[CellType.WALL for _ in range(size)] for _ in range(size)]
        maze._grid[start_x][start_y] = CellType.START
        maze._grid[end_x][end_y] = CellType.END

        def carve(x: int, y: int):
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx*2, y + dy*2  # Saltar una celda
                if 0 <= nx < size and 0 <= ny < size and maze._grid[nx][ny] == CellType.WALL:
                    maze._grid[x+dx][y+dy] = CellType.EMPTY  # Celda intermedia
                    maze._grid[nx][ny] = CellType.EMPTY
                    carve(nx, ny)

        # Comenzar desde una celda impar (para el algoritmo)
        start_cell_x, start_cell_y = random.choice([
            (x, y) for x in range(1, size-1, 2) 
            for y in range(1, size-1, 2)
        ])
        carve(start_cell_x, start_cell_y)

        return maze

    @staticmethod
    def ensure_connection(maze: Maze) -> None:
        """
        Garantiza que haya al menos un camino entre inicio y fin.
        """
        from .maze_solver import MazeSolver
        
        if not MazeSolver.has_solution(maze):
            # Conectar manualmente si no hay solución
            path = MazeSolver.find_path(maze, maze._start, maze._end)
            for x, y in path:
                maze._grid[x][y] = CellType.EMPTY
                