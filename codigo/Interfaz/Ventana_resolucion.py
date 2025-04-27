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
        self.fin = (self.filas-1, self.columnas-1)
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
        self.laberinto.datos[self.inicio[0]][self.inicio[1]] = 1
        self.laberinto.datos[self.fin[0]][self.fin[1]] = 1
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

        for item in self.items_solucion:
            self.scene.removeItem(item)
        self.items_solucion.clear()

        resultado = self.laberinto.solucionarMatriz(list(self.inicio), list(self.fin))

        if resultado:
            cell_size = 30
            pen = QPen(QColor("#3498db"), 2)

            caminos = self.laberinto.soluciones
            if caminos:
                camino = min(caminos, key=len)
                for paso in camino:
                    i, j = paso
                    rect = self.scene.addRect(
                        j*cell_size, i*cell_size, cell_size, cell_size,
                        pen, QColor(52, 152, 219, 100)
                    )
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
