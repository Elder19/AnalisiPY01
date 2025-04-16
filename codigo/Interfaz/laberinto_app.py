import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                              QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QFrame, QSpacerItem, 
                              QSizePolicy, QGridLayout, QGraphicsView, 
                              QGraphicsScene)
from PySide6.QtCore import (QPropertyAnimation, QTimer, Qt, 
                           QPoint, QEasingCurve, QSize)
from PySide6.QtGui import QPen, QColor

class VentanaBase(QMainWindow):
    """Clase base para VentanaJuego y VentanaResolucion"""
    def __init__(self, parent=None, titulo="Laberinto Mágico"):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumSize(800, 600)
        
        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        
        # Layout principal
        self.layout_principal = QHBoxLayout()
        self.widget_central.setLayout(self.layout_principal)
        
        # Menú hamburguesa (inicialmente oculto)
        self.menu_widget = QWidget()
        self.menu_widget.setObjectName("menu_widget")
        self.menu_widget.setFixedWidth(0)  # Comienza colapsado
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setContentsMargins(10, 20, 10, 20)
        self.menu_widget.setLayout(self.menu_layout)
        
        # Animación del menú
        self.menu_animation = QPropertyAnimation(self.menu_widget, b"minimumWidth")
        self.menu_animation.setDuration(300)
        self.menu_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # Botones del menú
        self.btn_inicio = QPushButton("Inicio")
        self.btn_inicio.setObjectName("btn_menu")
        self.btn_guardar = QPushButton("Guardar solución")
        self.btn_guardar.setObjectName("btn_menu")
        self.btn_cargar = QPushButton("Cargar solución")
        self.btn_cargar.setObjectName("btn_menu")
        
        self.menu_layout.addWidget(self.btn_inicio)
        self.menu_layout.addWidget(self.btn_guardar)
        self.menu_layout.addWidget(self.btn_cargar)
        self.menu_layout.addStretch()
        
        # Botón para mostrar/ocultar menú
        self.btn_menu = QPushButton("☰")
        self.btn_menu.setObjectName("btn_hamburguesa")
        self.btn_menu.setFixedSize(40, 40)
        self.btn_menu.clicked.connect(self.toggle_menu)
        
        # Área principal
        self.area_principal = QWidget()
        self.area_principal_layout = QVBoxLayout()
        self.area_principal.setLayout(self.area_principal_layout)
        
        # Layout para organizar todo
        self.main_content = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        self.top_bar.addWidget(self.btn_menu)
        self.top_bar.addStretch()
        
        self.main_content.addLayout(self.top_bar)
        self.main_content.addWidget(self.area_principal)
        
        # Añadir al layout principal
        self.layout_principal.addWidget(self.menu_widget)
        self.layout_principal.addLayout(self.main_content)
        
        # Conexiones comunes
        self.btn_inicio.clicked.connect(self.volver_inicio)
        
        # Cargar estilos
        self.cargar_estilos()
    
    def toggle_menu(self):
        """Muestra/oculta el menú lateral con animación"""
        current_width = self.menu_widget.width()
        if current_width == 0:
            # Animación para mostrar
            self.menu_animation.setStartValue(0)
            self.menu_animation.setEndValue(200)
            self.menu_animation.start()
        else:
            # Animación para ocultar
            self.menu_animation.setStartValue(200)
            self.menu_animation.setEndValue(0)
            self.menu_animation.start()
    
    def volver_inicio(self):
        """Vuelve a la ventana principal"""
        self.parent().show()
        self.close()
    
    def cargar_estilos(self):
        """Carga los estilos CSS"""
        try:
            with open('estilos.css', 'r') as file:
                estilo = file.read()
                self.setStyleSheet(estilo)
        except FileNotFoundError:
            print("¡Advertencia: Archivo estilos.css no encontrado!")

class VentanaJuego(VentanaBase):
    def __init__(self, parent=None):
        super().__init__(parent, "Laberinto Mágico - Juego")
        
        # Cuadrícula del laberinto
        self.grid_widget = QGraphicsView()
        self.scene = QGraphicsScene()
        self.grid_widget.setScene(self.scene)
        self.area_principal_layout.addWidget(self.grid_widget)
        
        # Botón de solución
        self.btn_solucion = QPushButton("Mostrar solución más óptima")
        self.btn_solucion.setObjectName("btn_solucion")
        self.area_principal_layout.addWidget(self.btn_solucion)
        self.btn_solucion.clicked.connect(self.mostrar_solucion)
        
        # Conexiones específicas
        self.btn_guardar.clicked.connect(self.guardar_solucion)
        self.btn_cargar.clicked.connect(self.cargar_solucion)
        
        # Dibujar cuadrícula inicial
        self.dibujar_cuadricula(10, 10)  # 10x10 por defecto
    
    def dibujar_cuadricula(self, filas, columnas):
        """Dibuja una cuadrícula en el área de juego"""
        self.scene.clear()
        cell_size = 30
        pen = QPen(Qt.GlobalColor.black)
        
        for i in range(filas):
            for j in range(columnas):
                rect = self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size)
                rect.setPen(pen)
    
    def guardar_solucion(self):
        print("Guardando solución del juego...")
    
    def cargar_solucion(self):
        print("Cargando solución del juego...")
    
    def mostrar_solucion(self):
        print("Mostrando solución óptima del juego...")

class VentanaResolucion(VentanaBase):
    def __init__(self, parent=None):
        super().__init__(parent, "Laberinto Mágico - Resolución")
        
        # Cuadrícula del laberinto
        self.grid_widget = QGraphicsView()
        self.scene = QGraphicsScene()
        self.grid_widget.setScene(self.scene)
        self.area_principal_layout.addWidget(self.grid_widget)
        
        # Conexiones específicas
        self.btn_guardar.clicked.connect(self.guardar_solucion)
        self.btn_cargar.clicked.connect(self.cargar_solucion)
        
        # Dibujar cuadrícula inicial
        self.dibujar_cuadricula(10, 10)  # 10x10 por defecto
    
    def dibujar_cuadricula(self, filas, columnas):
        """Dibuja una cuadrícula en el área de resolución"""
        self.scene.clear()
        cell_size = 30
        pen = QPen(Qt.GlobalColor.black)
        
        for i in range(filas):
            for j in range(columnas):
                rect = self.scene.addRect(j * cell_size, i * cell_size, cell_size, cell_size)
                rect.setPen(pen)
    
    def guardar_solucion(self):
        print("Guardando solución de resolución...")
    
    def cargar_solucion(self):
        print("Cargando solución de resolución...")

class VentanaLaberinto(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración inicial
        self.setWindowTitle("Laberinto Mágico")
        self.setMinimumSize(600, 400)
        
        # Widget central
        self.widget_central = QWidget()
        self.widget_central.setObjectName("ventana_principal")
        self.setCentralWidget(self.widget_central)
        
        # Layout principal
        self.layout_principal = QVBoxLayout()
        self.widget_central.setLayout(self.layout_principal)
        
        # Cargar estilos CSS
        self.cargar_estilos()
        
        # Componentes
        self.crear_frame_bienvenida()
        self.crear_botones()
        
        # Mostrar animación inicial
        QTimer.singleShot(300, self.iniciar_animacion_salida)
    
    def cargar_estilos(self):
        """Carga los estilos desde el archivo CSS"""
        try:
            with open('estilos.css', 'r') as file:
                estilo = file.read()
                self.setStyleSheet(estilo)
        except FileNotFoundError:
            print("¡Advertencia: Archivo estilos.css no encontrado!")
    
    def crear_frame_bienvenida(self):
        """Crea el frame de bienvenida"""
        self.frame_bienvenida = QFrame()
        self.frame_bienvenida.setObjectName("frame_bienvenida")
        
        layout_bienvenida = QVBoxLayout()
        self.frame_bienvenida.setLayout(layout_bienvenida)
        
        self.label_bienvenida = QLabel("Bienvenido al Laberinto")
        self.label_bienvenida.setObjectName("label_bienvenida")
        
        # Configuración de alineación directamente en Python
        self.label_bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout_bienvenida.addWidget(self.label_bienvenida)
        self.layout_principal.addWidget(self.frame_bienvenida)
        
        # Configurar animaciones
        self.animacion = QPropertyAnimation(self.frame_bienvenida, b"windowOpacity")
        self.animacion.setDuration(500)
        self.animacion.setStartValue(1.0)
        self.animacion.setEndValue(0.0)
        self.animacion.finished.connect(self.mostrar_botones)
        
        self.animacion_posicion = QPropertyAnimation(self.frame_bienvenida, b"pos")
        self.animacion_posicion.setDuration(500)
        self.animacion_posicion.setEasingCurve(QEasingCurve.OutQuad)
    
    def crear_botones(self):
        """Crea los botones de acción"""
        self.contenedor_botones = QWidget()
        self.contenedor_botones.setObjectName("contenedor_botones")
        self.layout_botones = QHBoxLayout()
        self.contenedor_botones.setLayout(self.layout_botones)
        
        # Botones
        self.boton_juego = QPushButton("Juego")
        self.boton_juego.setObjectName("boton_juego")
        
        self.boton_resolucion = QPushButton("Resolución")
        self.boton_resolucion.setObjectName("boton_resolucion")
        
        # Añadir al layout
        self.layout_botones.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout_botones.addWidget(self.boton_juego)
        self.layout_botones.addWidget(self.boton_resolucion)
        self.layout_botones.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Añadir al layout principal (oculto inicialmente)
        self.layout_principal.addWidget(self.contenedor_botones)
        self.contenedor_botones.hide()
        
        # Conexiones
        self.boton_juego.clicked.connect(self.iniciar_juego)
        self.boton_resolucion.clicked.connect(self.mostrar_resolucion)
    
    def iniciar_animacion_salida(self):
        """Inicia la animación de salida"""
        pos_original = self.frame_bienvenida.pos()
        pos_final = QPoint(pos_original.x(), pos_original.y() + 50)
        self.animacion_posicion.setStartValue(pos_original)
        self.animacion_posicion.setEndValue(pos_final)
        
        self.animacion.start()
        self.animacion_posicion.start()
    
    def mostrar_botones(self):
        """Muestra los botones después de la animación"""
        self.frame_bienvenida.hide()
        self.contenedor_botones.show()
    
    def iniciar_juego(self):
        """Abre la ventana de juego"""
        self.hide()
        self.ventana_juego = VentanaJuego(self)
        self.ventana_juego.show()
    
    def mostrar_resolucion(self):
        """Abre la ventana de resolución"""
        self.hide()
        self.ventana_resolucion = VentanaResolucion(self)
        self.ventana_resolucion.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ventana = VentanaLaberinto()
    ventana.show()
    
    sys.exit(app.exec())