
from PySide6.QtWidgets import QPushButton, QGraphicsView, QGraphicsScene, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from Backend.matriz import matriz
from Interfaz.Ventana_base import VentanaBase


class VentanaResolucion(VentanaBase):
    def __init__(self, laberinto=None, parent=None):
        super().__init__(parent)
        if laberinto is not None: 
            self.laberinto = laberinto
            self.filas = laberinto.filas
            self.columnas = laberinto.columnas
        
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
        self.btn_solucion.setObjectName("btn_solucion")
        self.btn_solucion.clicked.connect(self.mostrar_solucion)
        self.area_principal_layout.addWidget(self.btn_solucion)
        
        # Eventos
        self.grid_widget.mousePressEvent = self.seleccionar_celda
        
        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_laberinto)
       
        
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
        """Permite seleccionar celdas para inicio/fin"""
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
                QMessageBox.warning(self, "Error", "¡Ubicación inválida!")

            
    def mostrar_solucion(self):
            
        if not self.laberinto:
            return
         # Limpiar solución anterior
    
         # Eliminar de la escena todos los items antiguos
       
        # Resolver laberinto
        resultado = self.laberinto.solucionarMatriz(list(self.inicio), list(self.fin))
        if resultado:
            self.scene.clear()
            self.items_solucion.clear()
            self.dibujar_laberinto()
            # Dibujar solución
            cell_size = 30
            pen = QPen(QColor("#3498db"), 2)
            caminos = self.laberinto.soluciones
            tomados=[]
            casillas = []
            if caminos:
                camino = min(caminos, key=len)
                if not camino in tomados:
                    for paso in camino:
                        i, j = paso
                        casillas.append(paso)
                        rect = self.scene.addRect(
                            j*cell_size, i*cell_size, cell_size, cell_size,
                            pen,QColor(52, 152, 219, 100) # Rojo semitransparente
                        )
                tomados.append(camino)  
                camino = max(caminos, key=len)
                    
                if not camino in tomados:
                    for paso in camino:
                        i, j = paso
                        #if not paso in casillas:   
                        rect = self.scene.addRect(
                            j*cell_size, i*cell_size, cell_size, cell_size,
                            pen,QColor(255, 0, 0, 100) # Rojo semitransparente
                            ) 
                tomados.append(camino)
                self.items_solucion.append(rect)
        else:
            QMessageBox.warning(self, "Error", "¡No hay solución posible!")

    def guardar_laberinto(self):
        """Guarda el laberinto actual"""
        if self.laberinto:
            self.laberinto.guardarMatriz()
            QMessageBox.information(self, "Guardado", "Laberinto guardado correctamente")
    
