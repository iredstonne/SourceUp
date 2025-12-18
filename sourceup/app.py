import sys
import signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from pathlib import Path
from sourceup.manifest import (
    APP_NAME,
    APP_VERSION_TAG_NAME
)
from sourceup.updater import check_if_new_update_is_available
from sourceup.ui.window.MainWindow import MainWindow

def assets_path() -> Path:
    return Path(__file__).resolve().parent / "assets"

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    app = QApplication()
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION_TAG_NAME)
    app.setWindowIcon(QIcon(str(assets_path() / "icon.png")))
    check_if_new_update_is_available(APP_VERSION_TAG_NAME)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
