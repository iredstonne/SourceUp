from typing import Optional
from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QStackedLayout,
    QSplitter, QListView, QPushButton, QComboBox, QLineEdit, QCheckBox, QLabel, QMessageBox
)

from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.library.ZoteroLibraryType import ZoteroLibraryType
from sourceup.ui.model.ZoteroLibraryListModel import ZoteroLibraryListModel

class ZoteroManageLibrariesDialogView(QWidget):
    def __init__(self, initial_libraries, parent: Optional[QWidget] =None):
        super().__init__(parent)
        self._list_model = ZoteroLibraryListModel()
        self._list_model.set_rows(initial_libraries)
        self._layout = QStackedLayout(self)
        self._layout.addWidget(self._build_splitter())
        self.setLayout(self._layout)
        self._post_init()

    @property
    def libraries(self):
        return self._list_model.row_items

    def _post_init(self):
        self._list_model.rowsInserted.connect(self._update_list_buttons)
        self._list_model.rowsRemoved.connect(self._update_list_buttons)
        self._list_model.modelReset.connect(self._update_list_buttons)
        self._update_list_buttons()
        self._list_view.selectionModel().currentChanged.connect(self._on_list_view_current_changed)
        self._on_list_view_current_changed(self._list_view.currentIndex(), QModelIndex())

    def _build_splitter(self):
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setStyleSheet("QSplitter::handle { background-color: #cccccc; }")
        self._splitter.addWidget(self._build_list_panel_host())
        self._splitter.addWidget(self._build_form_panel_host())
        return self._splitter

    def _build_list_panel_host(self) -> QWidget:
        self._list_panel_host = QWidget()
        self._list_panel_layout = QVBoxLayout(self._list_panel_host)
        self._list_panel_layout.addWidget(self._build_list_view())
        self._list_panel_layout.addWidget(self._build_list_buttons_host())
        return self._list_panel_host

    def _build_list_view(self):
        self._list_view = QListView()
        self._list_view.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self._list_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self._list_view.setModel(self._list_model)
        return self._list_view

    def _on_list_view_current_changed(self, _current_idx: QModelIndex, _previous_idx: QModelIndex):
        _previous_row = self._row(_previous_idx)
        _current_row = self._row(_current_idx)
        if _previous_row == _current_row:
            return
        if _current_row is not None:
            self._fill_library_form(self._list_model.row_item_at(_current_row))
        else:
            self._clear_library_form()
        self._update_list_buttons()

    def _build_list_buttons_host(self) -> QWidget:
        self._list_buttons_host = QWidget()
        self._list_buttons_layout = QHBoxLayout(self._list_buttons_host)
        self._list_buttons_layout.addWidget(self._build_list_new_button())
        self._list_buttons_layout.addWidget(self._build_list_delete_button())
        self._list_buttons_layout.addWidget(self._build_list_delete_all_button())
        return self._list_buttons_host

    def _build_list_new_button(self) -> QPushButton:
        self._list_new_button = QPushButton("New")
        self._list_new_button.setDefault(False)
        self._list_new_button.setAutoDefault(False)
        self._list_new_button.clicked.connect(self._on_list_new_item_button_clicked)
        return self._list_new_button

    def _on_list_new_item_button_clicked(self):
        self._clear_library_form()
        self._select_none()

    def _build_list_delete_button(self) -> QPushButton:
        self._list_delete_button = QPushButton("Delete")
        self._list_delete_button.setAutoDefault(False)
        self._list_delete_button.clicked.connect(self._on_list_delete_item_button_clicked)
        return self._list_delete_button

    def _on_list_delete_item_button_clicked(self):
        _current_row = self._current_row()
        if _current_row is not None:
            if self._confirm_undoable_action(
                "Delete",
                "Delete this library?\n"
                "This can't be undone",
            ):
                self._list_model.remove_row_item_at(_current_row)
                self._select_previous_row(_current_row)
                self._clear_library_form()

    def _build_list_delete_all_button(self) -> QPushButton:
        self._list_delete_all_button = QPushButton("Delete all")
        self._list_delete_all_button.setAutoDefault(False)
        self._list_delete_all_button.clicked.connect(self._on_list_delete_all_item_button_clicked)
        return self._list_delete_all_button

    def _on_list_delete_all_item_button_clicked(self):
        _row_count = self._list_model.rowCount()
        if self._confirm_undoable_action(
            "Delete all",
            f"Delete {_row_count}"
            f"{"libraries" if _row_count > 1 else "library"}?\n"
            "This can't be undone",
        ):
            self._list_model.set_rows([])
            self._select_none()
            self._clear_library_form()

    def _build_form_panel_host(self) -> QWidget:
        self._form_panel_host = QWidget()
        self._form_panel_layout = QVBoxLayout(self._form_panel_host)
        self._form_panel_layout.addWidget(self._build_form_host())
        return self._form_panel_host

    def _build_form_host(self) -> QWidget:
        self._form_host = QWidget()
        self._form_layout = QFormLayout(self._form_host)
        self._form_layout.addRow("Library Type", self._build_form_library_type_combo())
        self._form_layout.addRow("Library ID", self._build_form_library_id_input())
        self._form_layout.addRow(self._build_form_library_id_hint())
        self._form_layout.addRow("Private Access", self._build_form_private_access_checkbox())
        self._form_layout.addRow(self._build_form_private_access_host())
        self._form_layout.addRow(self._build_form_commit_button())
        return self._form_host

    def _build_form_library_type_combo(self) -> QComboBox:
        self._form_library_type_combo = QComboBox()
        for _library_type_option in ZoteroLibraryType:
            self._form_library_type_combo.addItem(
                _library_type_option.name.capitalize(),
                _library_type_option
            )
        self._form_library_type_combo.currentIndexChanged.connect(lambda current_index: self._on_form_library_type_current_index_changed(self._form_library_type_combo.itemData(current_index)))
        return self._form_library_type_combo

    def _build_form_library_id_input(self) -> QLineEdit:
        self._form_library_id_input = QLineEdit()
        return self._form_library_id_input

    def _build_form_library_id_hint(self) -> QLabel:
        self._form_library_id_hint = QLabel()
        self._form_library_id_hint.setTextFormat(Qt.TextFormat.RichText)
        self._form_library_id_hint.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._form_library_id_hint.setWordWrap(True)
        self._form_library_id_hint.setOpenExternalLinks(True)
        self._on_form_library_type_current_index_changed(self._form_library_type_combo.itemData(self._form_library_type_combo.currentIndex()))
        return self._form_library_id_hint

    def _on_form_library_type_current_index_changed(self, _library_type: ZoteroLibraryType):
        match _library_type:
            case ZoteroLibraryType.USER:
                self._form_library_id_hint.setText(
                    "Enter a <b>User ID</b>. You can find it in your "
                    "<a href='https://www.zotero.org/settings/security#applications'>Zotero account settings → Security → Applications</a>"
                )
            case ZoteroLibraryType.GROUP:
                self._form_library_id_hint.setText(
                    "Enter a <b>Group ID</b> from your group's page on "
                    "<a href='https://www.zotero.org/groups/'>Zotero Groups</a>"
                )

    def _build_form_private_access_checkbox(self) -> QCheckBox:
        self._form_private_access_checkbox = QCheckBox()
        self._form_private_access_checkbox.setChecked(False)
        self._form_private_access_checkbox.toggled.connect(self._on_form_private_access_checkbox_toggled)
        return self._form_private_access_checkbox

    def _build_form_private_access_host(self) -> QWidget:
        self._form_private_access_host = QWidget()
        self._form_private_access_layout = QFormLayout(self._form_private_access_host)
        self._form_private_access_layout.addRow("Private Key", self._build_form_private_key_input())
        self._form_private_key_hint = QLabel()
        self._form_private_key_hint.setTextFormat(Qt.TextFormat.RichText)
        self._form_private_key_hint.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._form_private_key_hint.setWordWrap(True)
        self._form_private_key_hint.setOpenExternalLinks(True)
        self._form_private_key_hint.setText(
            "Create a new <b>Private Key</b> from your "
            "<a href='https://www.zotero.org/settings/security#applications'>Zotero account settings → Security → Applications</a>"
        )
        self._form_private_access_layout.addRow(self._form_private_key_hint)
        self._on_form_private_access_checkbox_toggled()
        return self._form_private_access_host

    def _on_form_private_access_checkbox_toggled(self):
        self._form_private_access_host.setVisible(self._form_private_access_checkbox.isChecked())

    def _build_form_private_key_input(self) -> QLineEdit:
        self._form_private_key_input = QLineEdit()
        self._form_private_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._form_private_key_input.setMaxLength(24)
        return self._form_private_key_input

    def _build_form_commit_button(self) -> QPushButton:
        self._form_commit_button = QPushButton("Save")
        self._form_commit_button.setDefault(False)
        self._form_commit_button.setAutoDefault(False)
        self._form_commit_button.clicked.connect(self._commit_library_form)
        return self._form_commit_button

    def _update_list_buttons(self):
        _has_rows = self._list_model.rowCount() > 0
        _has_current_row = self._current_row() is not None
        self._list_delete_button.setEnabled(_has_rows and _has_current_row)
        self._list_delete_all_button.setEnabled(_has_rows)
        self._update_form_commit_button()

    def _update_form_commit_button(self):
        _current_row = self._current_row()
        if _current_row is not None:
            self._form_commit_button.setText("Save")
        else:
            self._form_commit_button.setText("Add")

    def _clear_library_form(self):
        self._form_library_type_combo.setCurrentIndex(self._form_library_type_combo.findData(ZoteroLibraryType.USER))
        self._form_library_id_input.clear()
        self._form_private_access_checkbox.setChecked(False)
        self._form_private_key_input.clear()
        self._form_library_id_input.clearFocus()
        self._update_form_commit_button()

    def _fill_library_form(self, _saved_library: ZoteroLibrary):
        self._form_library_type_combo.setCurrentIndex(self._form_library_type_combo.findData(_saved_library.library_type))
        self._form_library_id_input.setText(_saved_library.library_id)
        self._form_private_access_checkbox.setChecked(bool(_saved_library.private_key))
        self._form_private_key_input.setText(_saved_library.private_key)
        self._form_library_id_input.setFocus()
        self._update_form_commit_button()

    def _read_library_form(self) -> ZoteroLibrary:
        _library_type = self._form_library_type_combo.itemData(self._form_library_type_combo.currentIndex()) or ZoteroLibraryType.USER
        _library_id = (self._form_library_id_input.text() or "").strip()
        _private_key = (self._form_private_key_input.text() or "").strip()
        return ZoteroLibrary(
            _library_type,
            _library_id,
            _private_key
        )

    @staticmethod
    def _row(_idx: QModelIndex) -> int:
        return _idx.row() if _idx.isValid() else None

    def _current_row(self) -> int:
        return self._row(self._list_view.currentIndex())

    def _select_row(self, _row: int):
        idx = self._list_model.index(_row)
        self._list_view.setCurrentIndex(idx)
        self._list_view.scrollTo(idx)

    def _select_none(self):
        self._list_view.setCurrentIndex(QModelIndex())

    def _select(self, _row: int):
        if 0 <= _row < self._list_model.rowCount():
            self._select_row(_row)
        else:
            self._select_none()

    def _select_last_row(self):
        self._select(self._list_model.rowCount() - 1)

    def _select_previous_row(self, _row: int):
        self._select(min(_row, self._list_model.rowCount() - 1))

    def _commit_library_form(self):
        _library_form = self._read_library_form()
        if not _library_form.library_id:
            self._form_library_id_input.setFocus()
            self._alert_missing_field(
                "Missing Library ID",
                "Please provide a valid Library ID"
            )
            return
        if self._form_private_access_checkbox.isChecked() and not _library_form.private_key:
            self._form_private_key_hint.setFocus()
            self._alert_missing_field(
                "Missing Private Key",
                "Please provide a valid Private Key"
            )
            return
        _current_row = self._current_row()
        if _current_row is not None:
            self._list_model.replace_row_item_at(
                _current_row,
                _library_form
            )
        else:
            self._list_model.append_row_item(
                _library_form
            )
            self._select_last_row()

    def _confirm_undoable_action(self, title: str, text: str):
        _message_box = QMessageBox(self)
        _message_box.setIcon(QMessageBox.Icon.Warning)
        _message_box.setWindowTitle(title)
        _message_box.setText(text)
        _message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        _message_box.setDefaultButton(QMessageBox.StandardButton.No)
        return _message_box.exec() == QMessageBox.StandardButton.Yes

    def _alert_missing_field(self, title: str, text: str):
        _message_box = QMessageBox(self)
        _message_box.setIcon(QMessageBox.Icon.Warning)
        _message_box.setWindowTitle(title)
        _message_box.setText(text)
        _message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        _message_box.setDefaultButton(QMessageBox.StandardButton.Ok)
        return _message_box.exec() == QMessageBox.StandardButton.Ok
