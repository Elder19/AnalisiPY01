import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#ccc
from PySide6.QtWidgets import QApplication
from Interfaz.Ventana_laberinto import VentanaLaberinto

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLaberinto()
    ventana.showFullScreen()
    sys.exit(app.exec())
