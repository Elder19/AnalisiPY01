from PySide6.QtWidgets import QPushButton, QGraphicsView, QGraphicsScene, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from Backend.matriz import matriz
from Interfaz.Ventana_base import VentanaBase

class VentanaJuego(VentanaBase):
    """ constructor of the class contains the metrods to draw, botton and ecents 
        """
    def __init__(self, laberinto=None, parent=None):
        super().__init__(parent)
        if laberinto is not None: 
            self.laberinto = laberinto
            self.filas = laberinto.filas
            self.columnas = laberinto.columnas
        self.inicio = None
        self.fin = self.laberinto.puntoFInal()
        self.contador = 0

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
        self.btn_confirmar_inicio = QPushButton("Jugar")
        self.btn_confirmar_inicio.setObjectName("btn_confirmar")
        self.btn_confirmar_inicio.clicked.connect(self.iniciar_movimiento)
        self.area_principal_layout.addWidget(self.btn_confirmar_inicio)
        
        self.btn_solucion.setObjectName("btn_solucion")
        self.btn_solucion.clicked.connect(self.mostrar_solucion)
        self.area_principal_layout.addWidget(self.btn_solucion)
        
        self.btn_solucion2 = QPushButton("siguiente Solución")
        self.btn_solucion2.setObjectName("btn_solucion")
        self.btn_solucion2.clicked.connect(self.siguiente_solucion)
        self.area_principal_layout.addWidget(self.btn_solucion2)
        self.btn_solucion2.setEnabled(False)
        # Eventos
       
        
        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_laberinto)
        self.dibujar_laberinto()
   
    
    """ make that user can use wasd to resolve the maze
        Args:
        Returns:
        Raises:
            QMessageBox if the position is not valid 
        """
    
    def iniciar_movimiento(self):
        self.trail_items.clear()
        self.dibujar_laberinto()
        self.inicio =self.laberinto.puntoFInal()
        if self.inicio == self.fin:
            self.iniciar_movimiento(self)
    
            
      
        self.btn_confirmar_inicio.setEnabled(False)
        """Activa el modo de movimiento del jugador"""
        if self.laberinto.datos[self.inicio[0]][self.inicio[1]] == 0:
            QMessageBox.warning(self, "Error", "La posición inicial debe estar en un pasillo (celda blanca)")
            return

        self.juego_activo = True
        self.posicion_actual = self.inicio
        self.dibujar_laberinto()  # Redibujar con el jugador
        self.grid_widget.setFocus()  # Asegura que reciba eventos de teclado
        
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
            self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size, pen, QColor(243, 156, 18, 150))
        if self.inicio is not None:
            # Marcar inicio y fin
            i, j = self.inicio
            self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#27ae60"))

        i, j = self.fin
        self.scene.addEllipse(j * cell_size + 5, i * cell_size + 5, 20, 20, pen, QColor("#e74c3c"))

        # Dibujar jugador
        if self.juego_activo and self.posicion_actual:
            i, j = self.posicion_actual
            self.scene.addEllipse(j * cell_size + 8, i * cell_size + 8, 14, 14, QPen(Qt.black), QColor("#f1c40f"))
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
    """ call the class matrix to resolve the maze and save the solution in soliuciones
        Args:
        Returns:
            printearSolucion: to draw the solution in the scene
        Raises:
            error if the maze is not possible to resolve
        """        
    def mostrar_solucion(self):
        self.btn_confirmar_inicio.setEnabled(True)
      
        if not self.laberinto:
            return
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
            self.pen = QPen(QColor("#3498db"), 2)
            self.camino =self.laberinto.soluciones[Nsolucion]
            
            for paso in range(len(self.camino)):
                       
                i, j = self.camino[paso]
                rect = self.scene.addRect(
                j*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size,
                self.pen,QColor(52, 152, 219, 100) # Rojo semitransparente
                )
                self.items_solucion.append(rect)
    """ detect WASD keys to move the player in the maze
        Args:
           event: event to detect the key pressed
        Returns:
           return the user looks the street to resolve the maze
        Raises:
        """          
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
                    self.btn_confirmar_inicio.setEnabled(True)
                    QMessageBox.information(self, "¡Llegaste!", "¡Has llegado al final del laberinto!")
                    self.juego_activo = False
     
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
    