from PySide6.QtWidgets import QMainWindow, QPushButton, QDialog

from sourceup.window.manage_zotero_libraries import ManageZoteroLibrariesWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SourceUp")
        self.setFixedSize(1280, 720)
        self._button = QPushButton("Manage Zotero Libraries", self)
        self._button.clicked.connect(self._open_manage_zotero_libraries)
        self.setCentralWidget(self._button)

    def _open_manage_zotero_libraries(self):
        dialog = ManageZoteroLibrariesWindow()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            print(dialog.libraries)
