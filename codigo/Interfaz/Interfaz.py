import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class VentanaBienvenida(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido")
        self.setGeometry(100, 100, 600, 300)  # más ancho para que se vea la barra lateral
        self.init_ui()

    def init_ui(self):
        # Crear widget central y layout principal (horizontal)
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Layout para menú lateral
        menu_layout = QVBoxLayout()

        # Botones del menú lateral
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar)

        btn_info = QPushButton("Acerca de")
        btn_info.clicked.connect(self.mostrar_info)

        btn_salir = QPushButton("Salir")
        btn_salir.clicked.connect(self.close)

        # Agregar botones al menú
        menu_layout.addWidget(btn_guardar)
        menu_layout.addWidget(btn_info)
        menu_layout.addWidget(btn_salir)
        menu_layout.addStretch()  # Empuja los botones hacia arriba

        # Layout del contenido principal
        contenido_layout = QVBoxLayout()

        self.label = QLabel("¡Bienvenido al laberinto!")
        self.label.setFont(QFont("Arial", 14))
        self.label.setAlignment(Qt.AlignCenter)

        self.boton = QPushButton("Comenzar")
        self.boton.setFont(QFont("Arial", 12))
        self.boton.clicked.connect(self.continuar)

        contenido_layout.addWidget(self.label)
        contenido_layout.addWidget(self.boton)
        contenido_layout.addStretch()

        # Añadir los dos layouts al principal
        main_layout.addLayout(menu_layout)
        main_layout.addLayout(contenido_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def guardar(self):
        QMessageBox.information(self, "Guardar", "Has hecho clic en Guardar.")

    def mostrar_info(self):
        QMessageBox.information(self, "Acerca de", "Este es un menú lateral en PyQt.")

    def continuar(self):
        print("Aquí empieza la aplicación...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaBienvenida()
    ventana.show()
    sys.exit(app.exec_())
