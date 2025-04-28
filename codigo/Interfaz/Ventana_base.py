import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

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
      
        self.menu_layout.addWidget(self.btn_inicio)
        self.menu_layout.addWidget(self.btn_guardar)
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
        if self.parent():
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
    
    def cambiar_central_widget(self, nuevo_widget):
        """Cambia el contenido de la ventana."""
        self.layout_principal.removeWidget(self.area_principal)  # quitas el viejo
        self.area_principal.deleteLater()  # destruyes el viejo widget
        self.area_principal = nuevo_widget
        self.area_principal_layout = QVBoxLayout(self.area_principal)
        self.main_content.addWidget(self.area_principal)  
    
