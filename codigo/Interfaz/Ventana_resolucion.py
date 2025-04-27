from PySide6.QtWidgets import QPushButton, QGraphicsView, QGraphicsScene, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from Backend.matriz import matriz
from Interfaz.Ventana_base import VentanaBase

class VentanaResolucion(VentanaBase):
    def __init__(self, parent=None):
        super().__init__(parent, "Laberinto Mágico - Resolución")
        self.filas = 11
        self.columnas = 11
        self.laberinto = None
        self.inicio = (0, 0)
        
        self.items_solucion = []

        self.grid_widget = QGraphicsView()
        self.scene = QGraphicsScene()
        self.grid_widget.setScene(self.scene)
        self.area_principal_layout.addWidget(self.grid_widget)

        self.btn_mostrar_solucion = QPushButton("Mostrar Solución")
        self.btn_mostrar_solucion.setObjectName("btn_solucion")
        self.btn_mostrar_solucion.clicked.connect(self.mostrar_solucion)
        self.area_principal_layout.addWidget(self.btn_mostrar_solucion)

        self.grid_widget.mousePressEvent = self.seleccionar_celda

        self.btn_guardar.clicked.connect(self.guardar_laberinto)
        self.btn_cargar.clicked.connect(self.cargar_laberinto)

        self.inicializar_laberinto()

    def seleccionar_celda(self, event):
        pos = self.grid_widget.mapToScene(event.pos())
        col = int(pos.x() // 30)
        fila = int(pos.y() // 30)

        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            if event.button() == Qt.LeftButton:
                self.inicio = (fila, col)
            elif event.button() == Qt.RightButton:
                self.fin = (fila, col)
            self.dibujar_laberinto()

    def inicializar_laberinto(self):
        self.laberinto = matriz(self.filas, self.columnas)
        self.fin = self.laberinto.puntoFInal()
        self.dibujar_laberinto()

    def dibujar_laberinto(self):
        self.scene.clear()
        cell_size = 30
        pen = QPen(Qt.black)

        for i in range(self.filas):
            for j in range(self.columnas):
                color = QColor("#2c3e50") if self.laberinto.datos[i][j] == 0 else QColor("#ecf0f1")
                self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size, pen, color)

        i, j = self.inicio
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#27ae60"))

        i, j = self.fin
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#e74c3c"))

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
            celdas_pintadas = set()
            if caminos:
                camino = min(caminos, key=len)
                if not camino in tomados:
                    for paso in camino:
                        if (i, j) not in celdas_pintadas:
                            i, j = paso
                            rect = self.scene.addRect(
                                j*cell_size, i*cell_size, cell_size, cell_size,
                                pen,QColor(52, 152, 219, 100) # Rojo semitransparente
                            )
                            celdas_pintadas.add((i, j))
                tomados.append(camino)  
                camino = max(caminos, key=len)
                    
                if not camino in tomados:
                    for paso in camino:
                        if (i, j) not in celdas_pintadas:
                            i, j = paso
                            rect = self.scene.addRect(
                                j*cell_size, i*cell_size, cell_size, cell_size,
                                pen,QColor(255, 0, 0, 100) # Rojo semitransparente
                            )
                            celdas_pintadas.add((i, j))
                tomados.append(camino)
                self.items_solucion.append(rect)
        else:
            QMessageBox.warning(self, "Error", "¡No hay solución posible!")

    def guardar_laberinto(self):
        if self.laberinto:
            self.laberinto.guardarMatriz()
            QMessageBox.information(self, "Guardado", "Laberinto guardado correctamente")

    def cargar_laberinto(self):
        try:
            self.laberinto = matriz(1, 1)
            self.laberinto.CargarMatriz()
            self.filas = len(self.laberinto.datos)
            self.columnas = len(self.laberinto.datos[0])
            self.dibujar_laberinto()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el laberinto:\n{str(e)}")
