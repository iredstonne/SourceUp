import sys
import signal
from PySide6.QtWidgets import QApplication
from sourceup.ui.window.MainWindow import MainWindow

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    app = QApplication()
    app.setApplicationName("SourceUp")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("SourceUp")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
