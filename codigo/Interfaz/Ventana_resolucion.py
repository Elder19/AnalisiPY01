from PySide6.QtWidgets import QPushButton, QGraphicsView, QGraphicsScene, QMessageBox, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from Backend.matriz import matriz
from Interfaz.Ventana_base import VentanaBase
import time

class VentanaResolucion(VentanaBase):
    """ constructor of the class contains the methods to draw, buttons and events """
    def __init__(self, laberinto=None, parent=None):
        super().__init__(parent)
        if laberinto is not None: 
            self.laberinto = laberinto
            self.filas = laberinto.filas
            self.columnas = laberinto.columnas
            self.resultado = []
        self.inicio = (0, 0)
        self.fin = self.laberinto.puntoFInal()
        self.contador = 0
    
        self.juego_activo = False
        self.posicion_actual = None
        self.trail_items = []
        self.items_solucion = []

        # Configuración inicial
        self.grid_widget = QGraphicsView()
        self.scene = QGraphicsScene()
        self.grid_widget.setScene(self.scene)
        self.area_principal_layout.addWidget(self.grid_widget)

        # Botones
        self.btn_solucion = QPushButton("Mostrar Solución")
        self.btn_solucion.setObjectName("btn_solucion")
        self.btn_solucion.clicked.connect(self.mostrar_solucion)

        self.btn_solucion2 = QPushButton("Siguiente Solución")
        self.btn_solucion2.setObjectName("btn_solucion")
        self.btn_solucion2.clicked.connect(self.siguiente_solucion)
        self.btn_solucion2.setEnabled(False)

        # Layout horizontal para los botones
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.btn_solucion)
        botones_layout.addWidget(self.btn_solucion2)

        botones_widget = QWidget()
        botones_widget.setLayout(botones_layout)
        self.area_principal_layout.addWidget(botones_widget)

        # Eventos
        self.grid_widget.mousePressEvent = self.seleccionar_celda

        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_laberinto)

        self.dibujar_laberinto()

    
    """ draw the maza in the scene and the start and end points
        Args:
        Returns:
        Raises:
        """
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
            self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size, pen, QColor("#2c3e50"))

        # Marcar inicio y fin
        i, j = self.inicio
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#27ae60"))

        i, j = self.fin
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#e74c3c"))

        # Dibujar jugador
        if self.juego_activo and self.posicion_actual:
            i, j = self.posicion_actual
            self.scene.addEllipse(j * cell_size + 8, i * cell_size + 8, 14, 14, QPen(Qt.black), QColor("#f1c40f"))
    """select the cell to start point
        Args:
        Returns:
           return datos in a list
        Raises:
            execpt if  FileNotFoundError,JSONDecodeError
        """
    def seleccionar_celda(self, event):
        """Permite seleccionar celdas para inicio/fin"""
        pos = self.grid_widget.mapToScene(event.pos())
        col = int(pos.x() // 30)
        fila = int(pos.y() // 30)
       
                
        if 0 <= fila < self.filas and 0 <= col < self.columnas and (fila, col) != self.fin:
            if self.laberinto.datos[fila][col] == 1: 
                if event.button() == Qt.LeftButton:
                    self.inicio = (fila, col)
                elif event.button() == Qt.RightButton:
                    self.fin = (fila, col)
                self.dibujar_laberinto()
            else:
                QMessageBox.warning(self, "Error", "¡Ubicación inválida!")

    """ call the class matrix to resolve the maze and save the solution in soliuciones
        Args:
        Returns:
            printearSolucion: to draw the solution in the scene
        Raises:
            error if the maze is not possible to resolve
        """        
    def mostrar_solucion(self):
            
        if not self.laberinto:
            return
         # Limpiar solución anterior
    
         # Eliminar de la escena todos los items antiguos
       
        # Resolver laberinto
        resultado = self.laberinto.solucionarMatriz(list(self.inicio), list(self.fin))
        if resultado:
            self.resultado = resultado
            self.btn_solucion2.setEnabled(True)
            self.printearSolucion(0)            
        else:
            QMessageBox.warning(self, "Error", "¡No hay solución posible!")
        
    """ draw the solution in the scene 
        Args:
            Nsolucion(int): position in the list of the maze 
        Returns:
           return the user looks the street to resolve the maze
        Raises:
        """
    def printearSolucion(self, Nsolucion):
            self.scene.clear()
            self.items_solucion.clear()
            self.dibujar_laberinto()
            # Dibujar solución
            self.cell_size = 30
            self.pen = QPen(QColor("#013708"), 2)
            
            self.camino =self.laberinto.soluciones[Nsolucion]

            t = (Nsolucion % 20) / 19  
            r = int(52 + (255 - 52) * t)         
            g = int(152 * (1 - t))               
            b = int(219 * (1 - t))              
            color = QColor(r, g, b, 150) 
 
                
            for paso in range(len(self.camino)):
                #time.sleep(0.5) 
                i, j = self.camino[paso]
                rect = self.scene.addRect(
                j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size,
                self.pen,color
                )
                self.items_solucion.append(rect)
              
    
    """ call clas matriz to execute guardarlaberinto
        Args:
            
        Returns:
           return QMessageBox if the maze is save else returns error 
        Raises:
        """
    def guardar_laberinto(self):

        """Guarda el laberinto actual"""
        if self.laberinto:
            resultado = self.laberinto.guardarMatriz()

            if resultado:
                QMessageBox.information(self, "Guardado", "Laberinto guardado correctamente")
            else:
         
                QMessageBox.information(self, "Guardado", "⚠️ El laberinto ya existe y no se guardó")
        else:
            QMessageBox.warning(self, "Error", "No hay laberinto para guardar")
    """ Call to printearSolucion  whith new position in the list to see other solutio
        Args:
            
        Returns:
           return printearSolucion(New position)
        Raises:
        """
    def siguiente_solucion(self):
        if self.contador== len(self.laberinto.soluciones)-1:
            self.contador=0
        self.contador+=1
        self.printearSolucion(self.contador)