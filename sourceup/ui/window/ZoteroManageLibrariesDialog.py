from typing import Optional, List
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QDialogButtonBox
from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.ui.window.ZoteroManageLibrariesDialogView import ZoteroManageLibrariesDialogView

class ZoteroManageLibrariesDialog(QDialog):
    def __init__(self, initial_libraries: List[ZoteroLibrary], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Manage Zotero Libraries")
        self.setFixedSize(1280, 720)
        self._dialog_layout = QVBoxLayout(self)
        self._dialog_view = ZoteroManageLibrariesDialogView(initial_libraries, self)
        self._dialog_layout.addWidget(self._dialog_view)
        self._dialog_buttons = QDialogButtonBox(self)
        self._dialog_buttons.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel) # type: ignore
        self._dialog_buttons.accepted.connect(self.accept)
        self._dialog_buttons.rejected.connect(self.reject)
        self._dialog_layout.addWidget(self._dialog_buttons)
        self.setLayout(self._dialog_layout)

    @property
    def libraries(self) -> List[ZoteroLibrary]:
        return self._dialog_view.libraries
