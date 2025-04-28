from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QSizePolicy, QGridLayout, QWidget, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from Backend import JsonM as jm
from Backend.matriz import matriz
class VentanaCargarSoluciones(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargar Soluciones")
        self.setFixedSize(1000, 1000)
        self.laberintos = jm.cargarDatos()
        self.Contador=len(self.laberintos)-1
        
       
        self.trail_items = []
        # >>> Aquí creamos el widget central <<<
        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        # Layout principal
        self.layout_principal = QVBoxLayout(self.widget_central)
        
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.layout_principal.addWidget(self.view)
        # Botones de Juego y Resolución
        self.contenedor_botones = QWidget(self.widget_central)
        self.contenedor_botones_layout = QHBoxLayout(self.contenedor_botones)

        self.Avanzar = QPushButton("-->", objectName="Avanzar")
        self.Retroceder = QPushButton("<--", objectName="Retroceder")
        
        self.Cancelar = QPushButton("Cancelar", objectName="Cancelar")
        self.Confirmar = QPushButton("Confirmar", objectName="Confirmar")
       
        self.Avanzar.clicked.connect(self.retroceder_laberinto)
        self.Retroceder.clicked.connect(self.avanzar_laberinto)
        self.Cancelar.clicked.connect(self.close)
        self.Confirmar.clicked.connect(self.guardar)
        
        self.contenedor_botones_layout.addWidget(self.Cancelar)
        self.contenedor_botones_layout.addWidget(self.Confirmar)
        
        self.contenedor_botones_layout.addStretch()
        self.contenedor_botones_layout.addWidget(self.Avanzar)
        self.contenedor_botones_layout.addWidget(self.Retroceder)
        self.contenedor_botones_layout.addStretch()

        # Añadimos el contenedor de botones al layout principal
        self.layout_principal.addWidget(self.contenedor_botones)
        self.cargar_laberinto(self.Contador)
    def guardar(self):
        if self.parent():
            self.parent().laberinto = self.laberinto
        self.close()   
        
    def cargar_laberinto(self,pos):
        try:
            self.laberinto = matriz(1, 1)  # Tamaño dummy
            self.laberinto.CargarMatriz(self.laberintos[pos])
            self.filas = len(self.laberinto.datos)
            self.columnas = len(self.laberinto.datos[0])
            self.dibujar_laberinto()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el laberinto:\n{str(e)}")
            
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
        

       
    def avanzar_laberinto(self):
        if self.Contador >= len(self.laberintos) :
            QMessageBox.information(self, "Fin", "No hay más laberintos para cargar.")
        
        if self.Contador < len(self.laberintos) - 1:
            self.Contador += 1
            self.cargar_laberinto(self.Contador)

    def retroceder_laberinto(self):
        if self.Contador >= len(self.laberintos) :
            QMessageBox.information(self, "Fin", "No hay más laberintos para cargar.")
          
        if self.Contador > 0:
            self.Contador -= 1
            self.cargar_laberinto(self.Contador)