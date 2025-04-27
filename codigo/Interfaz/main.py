from Interfaz.Ventana_laberinto import VentanaLaberinto
import sys
from PySide6.QtWidgets import (QApplication)
from Interfaz.Ventana_laberinto import VentanaLaberinto

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLaberinto()
    ventana.showFullScreen()
    sys.exit(app.exec())
