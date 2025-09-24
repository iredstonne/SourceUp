import sys
import signal
from PySide6.QtWidgets import QApplication
from sourceup.window.manage_zotero_libraries import ManageZoteroLibrariesWindow


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication()
    main_window = ManageZoteroLibrariesWindow()
    main_window.show()
    sys.exit(app.exec())
