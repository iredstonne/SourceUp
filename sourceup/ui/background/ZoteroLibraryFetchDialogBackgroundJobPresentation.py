from typing import Optional
from PySide6.QtWidgets import QWidget
from sourceup.ui.window.ZoteroLibraryFetchDialog import ZoteroLibraryFetchDialog

class ZoteroLibraryFetchDialogBackgroundJobPresentation:
    _dialog: Optional[ZoteroLibraryFetchDialog]

    def __init__(self):
        self._dialog = None

    def on_start(self, _parent: QWidget) -> None:
        self._dialog = ZoteroLibraryFetchDialog(_parent)
        self._dialog.show()

    def on_finish(self) -> None:
        if self._dialog:
            self._dialog.close()
            self._dialog.deleteLater()
            self._dialog = None
