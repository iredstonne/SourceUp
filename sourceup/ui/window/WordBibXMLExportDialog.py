from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QLabel

class WordBibXMLExportDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Word BibXML")
        self.setModal(True)
        self._layout = QVBoxLayout()
        self._label = QLabel("Exporting to Word BibXML…", self)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._label)
        self.setLayout(self._layout)
