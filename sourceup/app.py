import signal
import sys

from PySide6.QtWidgets import QApplication

from sourceup.window.main import MainWindow


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
