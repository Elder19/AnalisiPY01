from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt

class VentanaCargarSoluciones(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargar Soluciones")
        self.setFixedSize(1000, 1000)

        # Opcional: puedes agregar un texto de ejemplo en el centro
        label = QLabel("Aquí se cargarán las soluciones.", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 24px;
            color:
            #ffffff;
        """)
        self.setCentralWidget(label)
