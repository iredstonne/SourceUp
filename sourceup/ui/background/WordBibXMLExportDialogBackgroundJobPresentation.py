from typing import Optional
from PySide6.QtWidgets import QWidget
from sourceup.ui.dialog.WordBibXMLExportDialog import WordBibXMLExportDialog

class WordBibXMLExportDialogBackgroundJobPresentation:
    _dialog: Optional[WordBibXMLExportDialog]

    def __init__(self):
        self._dialog = None

    def on_start(self, _parent: QWidget) -> None:
        self._dialog = WordBibXMLExportDialog(_parent)
        self._dialog.show()

    def on_finish(self) -> None:
        if self._dialog:
            self._dialog.close()
            self._dialog.deleteLater()
            self._dialog = None
