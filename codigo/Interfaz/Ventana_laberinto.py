import sys
import random
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                              QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QSpacerItem, 
                              QSizePolicy, QGridLayout, QGraphicsView, 
                              QGraphicsScene, QMessageBox, QWidget, QGraphicsBlurEffect)
from PySide6.QtCore import (QPropertyAnimation, QTimer, Qt, 
                           QPoint, QEasingCurve, QRect)
from PySide6.QtGui import QPen, QColor
from Ventana_juego import VentanaJuego
from Ventana_resolucion import VentanaResolucion
from Backend.matriz import matriz

class VentanaLaberinto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laberinto Mágico")
        self.setMinimumSize(800, 600)
        self.label_click = QLabel(self)
        self.laberinto = None
        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # Layout base tipo Stack para superponer widgets
        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setAlignment(Qt.AlignCenter)

        # Contenedor de botones
        self.contenedor_botones = QWidget(self.widget_central)
        self.contenedor_botones.setFixedSize(500, 200)  # Ajusta según necesites
        self.contenedor_botones.move(
            (self.width() - self.contenedor_botones.width()) // 2,
            (self.height() - self.contenedor_botones.height()) // 2
        )
        self.contenedor_botones_layout = QHBoxLayout(self.contenedor_botones)

        self.boton_juego = QPushButton("Juego", objectName="boton_juego")
        self.boton_juego.clicked.connect(self.iniciar_juego)

        self.boton_resolucion = QPushButton("Resolución", objectName="boton_resolucion")
        self.boton_resolucion.clicked.connect(self.mostrar_resolucion)

        self.contenedor_botones_layout.addStretch()
        self.contenedor_botones_layout.addWidget(self.boton_juego)
        self.contenedor_botones_layout.addWidget(self.boton_resolucion)
        self.contenedor_botones_layout.addStretch()

        # Deshabilitar botones al inicio
        self.boton_juego.setEnabled(False)
        self.boton_resolucion.setEnabled(False)

        # Frame de bienvenida por encima
        self.frame_bienvenida = QFrame(self.widget_central, objectName="frame_bienvenida")
        self.frame_bienvenida.setStyleSheet("""
            #frame_bienvenida {
                background-color: rgba(52, 73, 94, 0.8); /* Semi-transparente */
                border-radius: 15px;
            }
        """)
        self.frame_bienvenida.setFixedSize(800, 600)
        self.frame_bienvenida.move(
            (self.width() - self.frame_bienvenida.width()) // 2,
            (self.height() - self.frame_bienvenida.height()) // 2
        )

        self.layout_bienvenida = QVBoxLayout(self.frame_bienvenida)
        self.layout_bienvenida.setAlignment(Qt.AlignCenter)

        self.label_bienvenida = QLabel("Bienvenido al juego Laberinto", objectName="label_bienvenida")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        self.label_bienvenida.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #ecf0f1;
        """)

        self.label_click = QLabel()
        self.label_click.setAlignment(Qt.AlignCenter)
        self.label_click.setStyleSheet("""
            font-size: 18px;
            color: #bdc3c7;
            font-style: italic;
        """)
        self.label_click.hide()

        self.layout_bienvenida.addWidget(self.label_bienvenida)
        self.layout_bienvenida.addWidget(self.label_click)

        # Evento de clic en bienvenida
        self.frame_bienvenida.mousePressEvent = self.mostrar_botones
        self.mensaje_listo = False


        # Cargar estilos CSS
        self.cargar_estilos()

        # Mensaje de click después de 2 segundos
        QTimer.singleShot(800, self.mostrar_mensaje_click)

            
        #Interfaz botones de tamaño
        self.BotonesTamaño= QWidget(self.widget_central)
        self.BotonesTamaño.setFixedSize(400,300)#tamano
        self.BotonesTamaño.move(
            self.width()-self.BotonesTamaño.width() -295,
            self.height()-self.BotonesTamaño.height() -290 )#margenes en el campo
        self.BotonesTamaño.setObjectName("BotonesTamaño")

        self.MatrizT = QGridLayout(self.BotonesTamaño)
        # Crear botones
        self.boton5 = QPushButton("5x5", objectName="mostrar_resolucion1")
        self.boton = QPushButton("10x10", objectName="mostrar_resolucion2")
        self.boton1 = QPushButton("15x15", objectName="mostrar_resolucion3")
        self.boton2 = QPushButton("20x20", objectName="mostrar_resolucion4")
        self.boton3 = QPushButton("25x25", objectName="mostrar_resolucion5")
        #llamar a la funcion crearLAB
        self.boton5.clicked.connect(lambda: self.crearLAB(5,5))
        self.boton.clicked.connect(lambda: self.crearLAB(10,10))
        self.boton1.clicked.connect(lambda: self.crearLAB(15,15))
        self.boton2.clicked.connect(lambda: self.crearLAB(20,20))
        self.boton3.clicked.connect(lambda: self.crearLAB(25,25))
        # Agregar botones al layout
        self.MatrizT.addWidget(self.boton5, 0, 0)   # Fila 0, Columna 0
        self.MatrizT.addWidget(self.boton, 0, 1)   # Fila 0, Columna 0
        self.MatrizT.addWidget(self.boton1, 1, 0)  # Fila 0, Columna 1
        self.MatrizT.addWidget(self.boton2, 1, 1)  # Fila 1, Columna 0
        self.MatrizT.addWidget(self.boton3, 2, 0)  # Fila 1, Columna 1
        
    # Ajustar estilos opcionales
        self.boton.setStyleSheet("font-size: 14px; padding: 0px; background-color: #27ae60;width: 0px;  ")
        self.boton1.setStyleSheet("font-size: 14px; padding: 1px; background-color: #27ae60; width: 0px;")
        self.boton2.setStyleSheet("font-size: 14px; padding: 1px; background-color: #27ae60; width: 0px; ")
        self.boton3.setStyleSheet("font-size: 14px; padding: 1px; background-color: #27ae60; width: 0px;")
        self.boton5.setStyleSheet("font-size: 14px; padding: 1px; background-color: #27ae60; width: 0px;")
        #self.BotonesTamaño.setStyleSheet("background-color: #270;width: 200px;")

    def resizeEvent(self, event):
        """Reajustar posiciones si la ventana cambia de tamaño"""
        super().resizeEvent(event)
        if hasattr(self, 'contenedor_botones'):
            self.contenedor_botones.move(
                (self.width() - self.contenedor_botones.width()) // 2,
                (self.height() - self.contenedor_botones.height()) // 2
            )
        if hasattr(self, 'frame_bienvenida'):
            self.frame_bienvenida.move(
                (self.width() - self.frame_bienvenida.width()) // 2,
                (self.height() - self.frame_bienvenida.height()) // 2
            )

    def mostrar_mensaje_click(self):
        """Muestra el mensaje 'Realiza click para empezar' con animación"""
        self.label_click.setText("Realiza click para empezar")
        self.label_click.show()

        self.animacion_click = QPropertyAnimation(self.label_click, b"windowOpacity")
        self.animacion_click.setDuration(1000)
        self.animacion_click.setStartValue(1.0)
        self.animacion_click.setEndValue(0.5)
        self.animacion_click.setLoopCount(-1)
        self.animacion_click.start()

        self.mensaje_listo = True
        # Deshabilitar botones hasta que se haga clic

    def terminar_bienvenida(self):
        """Finaliza la animación de bienvenida y muestra los botones"""
        # Ocultar el frame de bienvenida después de la animación
        self.frame_bienvenida.hide()

        # Eliminar el efecto de desenfoque de los botones
        self.contenedor_botones.setGraphicsEffect(None)

        # Hacer visibles y habilitar los botones
        self.boton_juego.setEnabled(True)
        self.boton_resolucion.setEnabled(True)

    def mostrar_botones(self, event=None):
        """Desliza hacia abajo y desvanece la bienvenida"""
        if not self.mensaje_listo:
            return

        if hasattr(self, 'animacion_click'):
            self.animacion_click.stop()

        # Animación de opacidad (fade-out)
        self.animacion_opacidad = QPropertyAnimation(self.frame_bienvenida, b"windowOpacity")
        self.animacion_opacidad.setDuration(700)
        self.animacion_opacidad.setStartValue(1.0)
        self.animacion_opacidad.setEndValue(0.0)
        self.animacion_opacidad.setEasingCurve(QEasingCurve.OutCubic)

        # Animación de posición (slide down)
        self.animacion_posicion = QPropertyAnimation(self.frame_bienvenida, b"geometry")
        self.animacion_posicion.setDuration(700)
        geometry_inicial = self.frame_bienvenida.geometry()
        geometry_final = QRect(
            geometry_inicial.x(),
            geometry_inicial.y() + 850,  # Baja 100px
            geometry_inicial.width(),
            geometry_inicial.height()
        )
        self.animacion_posicion.setStartValue(geometry_inicial)
        self.animacion_posicion.setEndValue(geometry_final)
        self.animacion_posicion.setEasingCurve(QEasingCurve.OutCubic)

        # Ejecutar ambas animaciones juntas
        self.animacion_opacidad.start()
        self.animacion_posicion.start()

        self.animacion_opacidad.finished.connect(self.terminar_bienvenida)

    def cargar_estilos(self):
        """Carga los estilos CSS"""
        ruta_css = os.path.join(os.path.dirname(__file__), "estilos.css")
        try:
            with open(ruta_css, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de estilos en {ruta_css}")
        self.widget_central.setStyleSheet("""
            QWidget {
                background-image: url(Interfaz/fondo.webp);
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

    def iniciar_juego(self):
        self.ventana_juego = VentanaJuego(self)
        self.ventana_juego.showFullScreen()

    def mostrar_resolucion(self):
        self.ventana_resolucion = VentanaResolucion(laberinto=self.laberinto,parent=self)
        self.ventana_resolucion.showFullScreen()
    def crearLAB(self,fila,columna):
        print("Creando laberinto de tamaño:", fila, "x", columna)
        self.laberinto=matriz(fila,columna)
        

    def closeEvent(self, event):
        QApplication.quit()
    
    def keyPressEvent(self, event):
        """Confirma si desea salir al presionar ESC"""
        if event.key() == Qt.Key_Escape:
            respuesta = QMessageBox.question(
                self, "Salir", "¿Seguro que quieres salir del juego?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.close()
