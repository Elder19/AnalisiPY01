import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation

class VentanaBienvenida(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido")
        self.setGeometry(100, 100, 600, 300)
        self.init_ui()

    def init_ui(self):
        # Crear widget central y layout principal (horizontal)
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Layout para contenido principal
        contenido_layout = QVBoxLayout()
        
        self.label = QLabel("¡Bienvenido al laberinto!")
        self.label.setAlignment(Qt.AlignCenter)

        self.boton = QPushButton("Comenzar")
        self.boton.clicked.connect(self.toggle_menu)

        contenido_layout.addWidget(self.label)
        contenido_layout.addWidget(self.boton)
        contenido_layout.addStretch()

        # Layout para el menú lateral
        self.menu_layout = QVBoxLayout()

        # Botones del menú lateral
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar)

        btn_info = QPushButton("Acerca de")
        btn_info.clicked.connect(self.mostrar_info)

        btn_salir = QPushButton("Salir")
        btn_salir.clicked.connect(self.close)

        # Agregar botones al menú
        self.menu_layout.addWidget(btn_guardar)
        self.menu_layout.addWidget(btn_info)
        self.menu_layout.addWidget(btn_salir)
        self.menu_layout.addStretch()

        # Contenedor del menú lateral
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_layout)

        # Animación para el menú deslizante
        self.animation = QPropertyAnimation(self.menu_widget, b"geometry")
        self.animation.setDuration(300)  # Duración de la animación
        self.animation.setStartValue(QRect(-200, 0, 200, 300))  # Inicialmente oculto a la izquierda
        self.animation.setEndValue(QRect(0, 0, 200, 300))  # Al abrir, en su posición correcta

        # Botón para abrir/cerrar el menú lateral
        self.toggle_button = QPushButton("Abrir Menú")
        self.toggle_button.clicked.connect(self.toggle_menu)
        self.toggle_button.setFixedSize(150, 40)  # Ajustar tamaño si lo deseas
        contenido_layout.insertWidget(0, self.toggle_button)  # Moverlo al principio

        # Añadir el botón toggle al layout
        contenido_layout.addWidget(self.toggle_button)

        # Añadir layouts al principal
        main_layout.addWidget(self.menu_widget)
        main_layout.addLayout(contenido_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def toggle_menu(self):
        
        # Cambiar el botón de abrir/cerrar
        if self.animation.direction() == QPropertyAnimation.Forward:
            self.animation.setDirection(QPropertyAnimation.Backward)
            self.toggle_button.setText("Abrir Menú")
        else:
            self.animation.setDirection(QPropertyAnimation.Forward)
            self.toggle_button.setText("Cerrar Menú")

        # Ejecutar animación
        self.animation.start()

    def guardar(self):
        QMessageBox.information(self, "Guardar", "Has hecho clic en Guardar.")

    def mostrar_info(self):
        QMessageBox.information(self, "Acerca de", "Este es un menú lateral desplegable en PyQt.")

    def continuar(self):
        print("Aquí empieza la aplicación...")

    def ocultar(self):
        """Método para ocultar el botón 'Comenzar'"""
        self.boton.hide()
        print("Botón oculto")  # Mensaje para comprobar en consola

    def mostrar(self):
        """Método para mostrar el botón 'Comenzar'"""
        self.boton.show()
        print("Botón mostrado")  # Mensaje para comprobar en consola

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBienvenida()
    ventana.show()
    ventana.ocultar()  # Llamar a ocultar() para que el botón se oculte al iniciar
    sys.exit(app.exec_())
