
import random

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import (QApplication, QMainWindow, 
                              QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QSpacerItem, 
                              QSizePolicy, QGridLayout, QGraphicsView, 
                              QGraphicsScene, QMessageBox, QWidget, QGraphicsBlurEffect)
from PySide6.QtCore import (QPropertyAnimation, QTimer, Qt, 
                           QPoint, QEasingCurve)
from PySide6.QtGui import QPen, QColor
from Backend.matriz import matriz  # Importación del backend

class VentanaBase(QMainWindow):
    """Clase base para VentanaJuego y VentanaResolucion"""
    def __init__(self, parent=None, titulo="Laberinto Mágico"):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumSize(1000, 1000)
        
        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        
        # Layout principal
        self.layout_principal = QHBoxLayout()
        self.widget_central.setLayout(self.layout_principal)
        
        # Menú hamburguesa
        self.menu_widget = QWidget()
        self.menu_widget.setObjectName("menu_widget")
        self.menu_widget.setFixedWidth(0)
        self.menu_layout = QVBoxLayout()
        self.menu_widget.setLayout(self.menu_layout)
        
        # Animación del menú
        self.menu_animation = QPropertyAnimation(self.menu_widget, b"minimumWidth")
        self.menu_animation.setDuration(300)
        self.menu_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # Botones del menú
        self.btn_inicio = QPushButton("Inicio")
        self.btn_inicio.setObjectName("btn_menu")
        self.btn_guardar = QPushButton("Guardar Laberinto")
        self.btn_guardar.setObjectName("btn_menu")
        self.btn_cargar = QPushButton("Cargar Laberinto")
        self.btn_cargar.setObjectName("btn_menu")
        
        self.menu_layout.addWidget(self.btn_inicio)
        self.menu_layout.addWidget(self.btn_guardar)
        self.menu_layout.addWidget(self.btn_cargar)
        self.menu_layout.addStretch()
        
        # Botón hamburguesa
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setObjectName("btn_hamburguesa")
        self.btn_menu.setFixedSize(40, 40)
        self.btn_menu.clicked.connect(self.toggle_menu)
        
        # Área principal
        self.area_principal = QWidget()
        self.area_principal_layout = QVBoxLayout()
        self.area_principal.setLayout(self.area_principal_layout)
        
        # Layout principal
        self.main_content = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        self.top_bar.addWidget(self.btn_menu)
        self.top_bar.addStretch()
        self.main_content.addLayout(self.top_bar)
        self.main_content.addWidget(self.area_principal)
        
        self.layout_principal.addWidget(self.menu_widget)
        self.layout_principal.addLayout(self.main_content)
        
        # Conexiones
        self.btn_inicio.clicked.connect(self.volver_inicio)
        self.cargar_estilos()
    
    def toggle_menu(self):
        """Muestra/oculta el menú lateral"""
        width = self.menu_widget.width()
        self.menu_animation.setStartValue(width)
        self.menu_animation.setEndValue(200 if width == 0 else 0)
        self.menu_animation.start()
    
    def volver_inicio(self):
        """Regresa a la ventana principal"""
        self.parent().show()
        self.close()
    
    def cargar_estilos(self):
        """Carga los estilos CSS"""
        ruta_css = os.path.join(os.path.dirname(__file__), "estilos.css")
        try:
            with open(ruta_css, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de estilos en {ruta_css}")

class VentanaJuego(VentanaBase):
    def __init__(self, parent=None):
        super().__init__(parent, "Laberinto Mágico - Juego")
        self.filas = 15
        self.columnas = 15
        self.laberinto = matriz(self.filas, self.columnas)
        self.inicio = (0, 0)
        self.fin = (self.filas-1, self.columnas-1)
       

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
            if event.button() == Qt.LeftButton:
                self.inicio = (fila, col)
            elif event.button() == Qt.RightButton:
                self.fin = (fila, col)
            self.dibujar_laberinto()
    
    def mostrar_solucion(self):
        """Muestra el camino óptimo"""
        if not self.laberinto:
            return

        # Limpiar solución anterior
        for item in self.items_solucion:
            self.scene.removeItem(item)
        self.items_solucion.clear()

        # Resolver laberinto
        resultado = self.laberinto.solucionarMatriz(list(self.inicio), list(self.fin))

        if resultado:
            # Dibujar solución
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


class VentanaResolucion(VentanaBase):
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
        self.btn_solucion.setObjectName("btn_solucion")
        self.btn_solucion.clicked.connect(self.mostrar_solucion)
        self.area_principal_layout.addWidget(self.btn_solucion)
        
        # Eventos
        self.grid_widget.mousePressEvent = self.seleccionar_celda
        
        # Conexiones
        self.btn_guardar.clicked.connect(self.guardar_laberinto)
        self.btn_cargar.clicked.connect(self.cargar_laberinto)
        
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
            if event.button() == Qt.LeftButton:
                self.inicio = (fila, col)
    
            self.dibujar_laberinto()
            
    def mostrar_solucion(self):
        """Muestra el camino óptimo"""
        if not self.laberinto:
            return

        # Resolver laberinto
        resultado = self.laberinto.solucionarMatriz(list(self.inicio), list(self.fin))
        print  (resultado)
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
            
            
class VentanaLaberinto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laberinto Mágico")
        self.setMinimumSize(800, 600)

        # Widget central y layout principal
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout(self.widget_central)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes


        # Frame de bienvenida
        self.frame_bienvenida = QFrame(objectName="frame_bienvenida")
        self.frame_bienvenida.setStyleSheet("""
            #frame_bienvenida {
                background-color: rgba(52, 73, 94, 0.7);  /* Más transparente */
                border-radius: 15px;
                padding: 20px;
            }
        """)
        self.frame_bienvenida.setFixedSize(600, 400)  # ancho: 400px, alto: 250px
        self.frame_bienvenida.setGeometry(self.rect())  # Asegura que ocupe toda la pantalla
        self.layout_bienvenida = QVBoxLayout(self.frame_bienvenida)

        # Label de bienvenida
        self.label_bienvenida = QLabel("Bienvenido al juego Laberinto", objectName="label_bienvenida")
        self.label_bienvenida.setAlignment(Qt.AlignCenter)
        self.label_bienvenida.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #ecf0f1;
            padding: 20px;
        """)

        # Label de mensaje secundario
        self.label_click = QLabel()
        self.label_click.setAlignment(Qt.AlignCenter)
        self.label_click.setStyleSheet("""
            font-size: 18px;
            color: #bdc3c7;
            font-style: italic;
            padding: 10px;
        """)
        self.label_click.hide()

        # Agregar labels al layout de bienvenida
        self.layout_bienvenida.addWidget(self.label_bienvenida)
        self.layout_bienvenida.addWidget(self.label_click)

        # Contenedor de botones
        self.contenedor_botones = QWidget(objectName="contenedor_botones")
        self.layout_botones = QHBoxLayout(self.contenedor_botones)

        self.boton_juego = QPushButton("Juego", objectName="boton_juego")#INICIA VENTANA JUEGO
        self.boton_juego.clicked.connect(self.iniciar_juego)

        self.boton_resolucion = QPushButton("Resolhhhución", objectName="boton_resolucion")#INICIA VENTANA RESOLUCION
        self.boton_resolucion.clicked.connect(self.mostrar_resolucion)

        self.layout_botones.addStretch()
        self.layout_botones.addWidget(self.boton_juego)
        self.layout_botones.addWidget(self.boton_resolucion)
        self.layout_botones.addStretch()

        # Efecto blur al contenedor de botones (al inicio)
        self.blur_botones = QGraphicsBlurEffect()
        self.blur_botones.setBlurRadius(10)
        self.contenedor_botones.setGraphicsEffect(self.blur_botones)

        # Deshabilitar botones al inicio
        self.boton_juego.setEnabled(False)
        self.boton_resolucion.setEnabled(False)

        self.contenedor_botones.show()  # Mostrar desde el inicio pero con desenfoque

        # Agregar widgets al layout principal
        self.layout_principal.addWidget(self.frame_bienvenida)
        self.layout_principal.addWidget(self.contenedor_botones)

        # Cargar estilos
        self.cargar_estilos()

        # Evento de clic en el frame de bienvenida
        self.frame_bienvenida.mousePressEvent = self.mostrar_botones

        # Mostrar mensaje después de un tiempo
        QTimer.singleShot(2000, self.mostrar_mensaje_click)

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

    def mostrar_botones(self, event=None):
        """Oculta la bienvenida y muestra los botones nítidos"""
        if hasattr(self, 'animacion_click'):
            self.animacion_click.stop()

        self.frame_bienvenida.hide()

        # Quitar efecto blur de los botones
        self.contenedor_botones.setGraphicsEffect(None)

        # Habilitar los botones
        self.boton_juego.setEnabled(True)
        self.boton_resolucion.setEnabled(True)

    def cargar_estilos(self):
        """Carga los estilos CSS desde archivo"""
        ruta_css = os.path.join(os.path.dirname(__file__), "estilos.css")
        try:
            with open(ruta_css, 'r') as archivo:
                self.setStyleSheet(archivo.read())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de estilos en {ruta_css}")

    def iniciar_juego(self):
        """Lanza la ventana del juego"""
        self.hide()
        self.ventana_juego = VentanaJuego(self)
        self.ventana_juego.show()

    def mostrar_resolucion(self): # MUESTRA VENTANAS DE JUEGO 
        """Muestra mensaje o lanza modo resolución"""
        self.hide()
        self.ventana_resolucion = VentanaResolucion(self)
        self.ventana_resolucion.setWindowTitle("Laberinto Mágico - Resolución")
        self.ventana_resolucion.show()

    def closeEvent(self, event):
        """Cierra completamente la aplicación al cerrar la ventana principal"""
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLaberinto()
    ventana.show()
    sys.exit(app.exec())

