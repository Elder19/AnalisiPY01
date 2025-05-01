import sys
import random
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QSizePolicy, QGridLayout, QWidget, QMessageBox)
from PySide6.QtCore import Qt
from Ventana_juego import VentanaJuego
from Ventana_resolucion import VentanaResolucion
from Backend.matriz import matriz
from Ventana_cargar_soluciones import VentanaCargarSoluciones



class VentanaLaberinto(QMainWindow):
    """ Initializes the main labyrinth selection window.
        Sets up the window title, size, central widget, layouts, and UI elements
        like the main title, game/resolution buttons, size selection text,
        size buttons, and the 'Load Solutions' button.
        Args:
        Returns:
        Raises:
        """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laberinto Mágico")
        self.setMinimumSize(800, 600)
        self.laberinto = None

        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # Layout principal
        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(40, 40, 40, 20)
        self.layout_principal.setSpacing(30)
        self.layout_principal.setAlignment(Qt.AlignTop)

        # Titulo principal
        self.titulo = QLabel("Laberinto\nEl Desierto de la Confusión", self.widget_central)
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #B2C9AD;
        """)
        self.layout_principal.addWidget(self.titulo)

        # --> Aquí agregamos el espacio extra
        self.layout_principal.addSpacing(120)

        # Botones de Juego y Resolucion
        self.contenedor_botones = QWidget(self.widget_central)
        self.contenedor_botones_layout = QHBoxLayout(self.contenedor_botones)

        self.boton_juego = QPushButton("Juego", objectName="boton_juego")
        self.boton_juego.clicked.connect(self.iniciar_juego)

        self.boton_resolucion = QPushButton("Resolución", objectName="boton_resolucion")
        self.boton_resolucion.clicked.connect(self.mostrar_resolucion)

        self.contenedor_botones_layout.addStretch()
        self.contenedor_botones_layout.addWidget(self.boton_juego)
        self.contenedor_botones_layout.addWidget(self.boton_resolucion)
        self.contenedor_botones_layout.addStretch()


        self.layout_principal.addWidget(self.contenedor_botones)

        # Texto selecciona tamaño
        self.texto_tamano = QLabel("Selecciona el tamaño del laberinto", self.widget_central)
        self.texto_tamano.setAlignment(Qt.AlignCenter)
        self.texto_tamano.setStyleSheet("""
            font-size: 24px;
            color: #d4ffdb;
            margin-top: 100px;
        """)
        self.layout_principal.addWidget(self.texto_tamano)

        # Spacer para empujar hacia abajo
        self.layout_principal.addStretch()

        # Botones de tamaño
        self.BotonesTamaño = QWidget(self.widget_central)
        self.MatrizT = QGridLayout(self.BotonesTamaño)
        self.MatrizT.setSpacing(20)

        self.boton5 = QPushButton("5x5", objectName="mostrar_resolucion1")
        self.boton10 = QPushButton("10x10", objectName="mostrar_resolucion2")
        self.boton15 = QPushButton("15x15", objectName="mostrar_resolucion3")
        self.boton20 = QPushButton("20x20", objectName="mostrar_resolucion4")
        self.boton25 = QPushButton("25x25", objectName="mostrar_resolucion5")
        self.botonCarg = QPushButton("Cargar Soluciones", objectName="cargar_resoluciones")

        self.boton5.clicked.connect(lambda: self.crearLAB(5, 5))
        self.boton10.clicked.connect(lambda: self.crearLAB(10, 10))
        self.boton15.clicked.connect(lambda: self.crearLAB(15, 15))
        self.boton20.clicked.connect(lambda: self.crearLAB(20, 20))
        self.boton25.clicked.connect(lambda: self.crearLAB(25, 25))

        self.MatrizT.addWidget(self.boton5, 0, 0)
        self.MatrizT.addWidget(self.botonCarg, 0, 1)
        self.MatrizT.addWidget(self.boton10,1, 0)
        self.MatrizT.addWidget(self.boton15, 1, 1)
        self.MatrizT.addWidget(self.boton20, 2, 0)
        self.MatrizT.addWidget(self.boton25, 2, 1)

        self.layout_principal.addWidget(self.BotonesTamaño, alignment=Qt.AlignBottom)

        self.botonCarg.clicked.connect(self.mostrar_cargar_soluciones)

        # Estilos de botones de tamaño
        botones = [self.boton5, self.boton10, self.boton15, self.boton20, self.boton25, self.botonCarg]
        for boton in botones:
            boton.setStyleSheet("""
                font-size: 18px;
                padding: 12px;
                background-color: #91AC8F;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            """)

        botones = [self.botonCarg]
        for boton in botones:
            boton.setStyleSheet("""
                font-size: 18px;
                padding: 12px;
                background-color: #66785F;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            """)

        self.layout_principal.addWidget(self.BotonesTamaño)

        # Cargar estilos CSS
        self.cargar_estilos()

    """ Loads CSS styles from an external file and applies them to the window.
        Looks for the 'estilos.css' file in the same directory as the script.
        Args:
        Returns:
        Raises:
            FileNotFoundError: If the 'estilos.css' file is not found (handled internally with a print).
        """
    def cargar_estilos(self):
        ruta_css = os.path.join(os.path.dirname(__file__), "estilos.css")
        try:
            with open(ruta_css, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de estilos en {ruta_css}")
            
    """ Opens the game window if a labyrinth has been created.
        Displays a warning message if no labyrinth has been selected yet.
        Args:
        Returns:
        Raises:
        """
    def iniciar_juego(self):
        if self.laberinto is None:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar una dimensión de laberinto antes de jugar.")
            return
        self.ventana_juego = VentanaJuego(laberinto=self.laberinto, parent=self)
        self.ventana_juego.showFullScreen()

    """ Opens the resolution window if a labyrinth has been created.
        Displays a warning message if no labyrinth has been selected yet.
        Args:
        Returns:
        Raises:
        """
    def mostrar_resolucion(self):
        if self.laberinto is None:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar una dimensión de laberinto antes de jugar.")
            return
        self.ventana_resolucion = VentanaResolucion(laberinto=self.laberinto, parent=self)
        self.ventana_resolucion.showFullScreen()

    """ Creates a new labyrinth matrix with the specified dimensions.
        Assigns the newly created labyrinth to the self.laberinto attribute.
        Args:
            fila (int): The number of rows for the labyrinth.
            columna (int): The number of columns for the labyrinth.
        Returns:
        Raises:
        """
    def crearLAB(self, fila, columna):
        print("Creando laberinto de tamaño:", fila, "x", columna)
        self.laberinto = matriz(fila, columna)

    """ Handles the close event of the window.
        Exits the application when the window is closed.
        Args:
            event (QCloseEvent): The close event object.
        Returns:
        Raises:
        """
    def closeEvent(self, event):
        QApplication.quit()

    """ Handles key press events for the window.
        Specifically, it prompts the user to confirm if they want to exit
        when the Escape key is pressed.
        Args:
            event (QKeyEvent): The key event object.
        Returns:
        Raises:
        """
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            respuesta = QMessageBox.question(
                self, "Salir", "¿Seguro que quieres salir del juego?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.close()

    """ Opens the 'Load Solutions' window.
        Creates an instance of VentanaCargarSoluciones and displays it.
        Args:
        Returns:
        Raises:
        """
    def mostrar_cargar_soluciones(self):
        self.ventana_cargar = VentanaCargarSoluciones(self)
        self.ventana_cargar.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLaberinto()
    ventana.show()
    sys.exit(app.exec())
