import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from Interfaz.Ventana_laberinto import VentanaLaberinto

"""
This script serves as the main entry point for the application.
It configures the system path to allow module imports,
initializes the PySide6 application, creates and displays the main labyrinth window
in full screen, and starts the application's event loop.
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLaberinto()
    ventana.showFullScreen()
    sys.exit(app.exec())
