from PySide6.QtWidgets import QPushButton, QGraphicsView, QGraphicsScene, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from Backend.matriz import matriz
from Interfaz.Ventana_base import VentanaBase

class VentanaJuego(VentanaBase):
    def __init__(self, parent=None):
        super().__init__(parent, "Laberinto Mágico - Juego")
        self.filas = 20
        self.columnas = 20
        self.laberinto = matriz(self.filas, self.columnas)
        self.inicio = (0, 0)
        self.fin = self.laberinto.puntoFInal()
       

        self.juego_activo = False
        self.posicion_actual = None
        self.trail_items = []
        
        self.items_solucion = []  # ← después de self.fin = ...

        # Configuración inicial
        self.grid_widget = QGraphicsView()
        self.scene = QGraphicsScene()
        self.grid_widget.setScene(self.scene)
        self.area_principal_layout.addWidget(self.grid_widget)
        
        # Botones
        self.btn_solucion = QPushButton("Mostrar Solución")
        self.btn_confirmar_inicio = QPushButton("Confirmar Inicio")
        self.btn_confirmar_inicio.setObjectName("btn_confirmar")
        self.btn_confirmar_inicio.clicked.connect(self.iniciar_movimiento)
        self.area_principal_layout.addWidget(self.btn_confirmar_inicio)

        self.btn_solucion.setObjectName("btn_solucion")
        self.btn_solucion.clicked.connect(self.mostrar_solucion)
        self.area_principal_layout.addWidget(self.btn_solucion)
        
        # Eventos
        self.grid_widget.mousePressEvent = self.seleccionar_celda
        
        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_laberinto)
        self.btn_cargar.clicked.connect(self.cargar_laberinto)
        
        self.inicializar_laberinto()
    
    def seleccionar_celda(self, event):
        """Selecciona la celda de inicio si el juego no ha comenzado"""
        if self.juego_activo:
            return  # No permitir selección durante el juego

        pos = event.position().toPoint()
        pos = self.grid_widget.mapToScene(pos)
        col = int(pos.x() // 30)
        fila = int(pos.y() // 30)

        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            if event.button() == Qt.LeftButton:
                self.inicio = (fila, col)
                self.dibujar_laberinto()
    
    def iniciar_movimiento(self):
        """Activa el modo de movimiento del jugador"""
        if self.laberinto.datos[self.inicio[0]][self.inicio[1]] == 0:
            QMessageBox.warning(self, "Error", "La posición inicial debe estar en un pasillo (celda blanca)")
            return

        self.juego_activo = True
        self.posicion_actual = self.inicio
        self.dibujar_laberinto()  # Redibujar con el jugador
        self.grid_widget.setFocus()  # Asegura que reciba eventos de teclado

    def inicializar_laberinto(self):
        """Crea un nuevo laberinto con camino garantizado"""
        self.laberinto = matriz(self.filas, self.columnas)
        # Asegurar que inicio y fin sean caminos transitables
        self.laberinto.datos[self.inicio[0]][self.inicio[1]] = 1
        self.laberinto.datos[self.fin[0]][self.fin[1]] = 1
        self.dibujar_laberinto()

    def dibujar_laberinto(self):
        """Dibuja el laberinto en la escena"""
        self.scene.clear()
        cell_size = 30
        pen = QPen(Qt.black)

        # Dibuja las celdas
        for i in range(self.filas):
            for j in range(self.columnas):
                color = QColor("#2c3e50") if self.laberinto.datos[i][j] == 0 else QColor("#ecf0f1")
                self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size, pen, color)

        # Dibuja el contorno del laberinto (un borde alrededor)
        # Añade un rectángulo alrededor de toda la matriz
        borde_pen = QPen(Qt.black, 8)  # Borde grueso
        self.scene.addRect(0, 0, self.columnas * cell_size, self.filas * cell_size, borde_pen)
        
        # Volver a dibujar rastro
        cell_size = 30
        pen = QPen(Qt.NoPen)
        for paso in self.trail_items:
            i, j = paso
            self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size, pen, QColor(243, 156, 18, 150))

        # Marcar inicio y fin
        i, j = self.inicio
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#27ae60"))

        i, j = self.fin
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#e74c3c"))

        # Dibujar jugador
        if self.juego_activo and self.posicion_actual:
            i, j = self.posicion_actual
            self.scene.addEllipse(j * cell_size + 8, i * cell_size + 8, 14, 14, QPen(Qt.black), QColor("#f1c40f"))

    def seleccionar_celda(self, event):
         """Permite seleccionar celdas para inicio/fin antes de iniciar el juego"""
         if self.juego_activo:
             return  # No permitir cambiar inicio/fin después de iniciar el juego
 
         pos = self.grid_widget.mapToScene(event.pos())
         col = int(pos.x() // 30)
         fila = int(pos.y() // 30)
 
         if 0 <= fila < self.filas and 0 <= col < self.columnas:
             if self.laberinto.datos[fila][col] == 1:
                 if event.button() == Qt.LeftButton:
                     self.inicio = (fila, col)
                 elif event.button() == Qt.RightButton:
                     self.fin = (fila, col)
                 self.dibujar_laberinto()
             else:
                 QMessageBox.warning(self, "Error", "¡Ubicación inválida! Solo puedes seleccionar pasillos.")
    
    def mostrar_solucion(self):
        
        if not self.laberinto:
            return
         # Limpiar solución anterior
    
        self.items_solucion.clear()
        # Resolver laberinto
        resultado = self.laberinto.solucionarMatriz(list(self.inicio), list(self.fin))
        if resultado:
            # Dibujar solución
            cell_size = 30
            pen = QPen(QColor("#3498db"), 2)
            caminos = self.laberinto.soluciones
            tomados=[]
            if caminos:
                camino = min(caminos, key=len)
                if not camino in tomados:
                    for paso in camino:
                        i, j = paso
                        rect = self.scene.addRect(
                            j*cell_size, i*cell_size, cell_size, cell_size,
                            pen,QColor(52, 152, 219, 100) # Rojo semitransparente
                        )
                tomados.append(camino)  
                camino = max(caminos, key=len)
                    
                if not camino in tomados:
                    for paso in camino:
                        i, j = paso
                        rect = self.scene.addRect(
                            j*cell_size, i*cell_size, cell_size, cell_size,
                            pen,QColor(255, 0, 0, 100) # Rojo semitransparente
                        ) 
                tomados.append(camino)
                self.items_solucion.append(rect)
        else:
            QMessageBox.warning(self, "Error", "¡No hay solución posible!")

    def keyPressEvent(self, event):
        if not self.juego_activo or self.posicion_actual is None:
            return

        direcciones = {
            Qt.Key_W: (-1, 0),
            Qt.Key_S: (1, 0),
            Qt.Key_A: (0, -1),
            Qt.Key_D: (0, 1),
        }

        if event.key() in direcciones:
            dx, dy = direcciones[event.key()]
            x, y = self.posicion_actual
            nx, ny = x + dx, y + dy

            if (0 <= nx < self.filas and 0 <= ny < self.columnas and
                    self.laberinto.datos[nx][ny] == 1):

                # Pintar rastro
                cell_size = 30
                self.trail_items.append((nx, ny))

                self.posicion_actual = (nx, ny)

                # Redibujar jugador
                self.dibujar_laberinto()

                if self.posicion_actual == self.fin:
                    QMessageBox.information(self, "¡Llegaste!", "¡Has llegado al final del laberinto!")
                    self.juego_activo = False

    def guardar_laberinto(self):
        """Guarda el laberinto actual"""
        if self.laberinto:
            self.laberinto.guardarMatriz()
            QMessageBox.information(self, "Guardado", "Laberinto guardado correctamente")
    
    def cargar_laberinto(self):
        """Carga un laberinto guardado"""
        try:
            self.laberinto = matriz(1, 1)  # Tamaño dummy
            self.laberinto.CargarMatriz()
            self.filas = len(self.laberinto.datos)
            self.columnas = len(self.laberinto.datos[0])
            self.dibujar_laberinto()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el laberinto:\n{str(e)}")
