from PySide6.QtCore import Qt, QModelIndex, QRegularExpression, QTimer
from PySide6.QtGui import QRegularExpressionValidator, QValidator
from PySide6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QFormLayout,
    QDialog, QMessageBox,
    QWidget, QLineEdit, QPushButton, QListView, QComboBox, QCheckBox, QLabel, QDialogButtonBox, QSplitter, QStyle,
    QSizePolicy
)
from sourceup.data.zotero_library import ZoteroLibrary, LibraryType
from sourceup.model.zotero_library_model import ZoteroLibraryModel

class ValidatedLineEdit(QWidget):
    def __init__(self, input_: QLineEdit, validator: QValidator | None = None, parent=None):
        super().__init__(parent)
        self._input = input_
        if validator is not None:
            self._input.setValidator(validator)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._input, 1)
        self._input.textChanged.connect(self.on_text_changed)
        self._error_indicator_label = QLabel()
        self._error_indicator_label.setVisible(False)
        self._error_indicator_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        self._error_indicator_pixmap = self._error_indicator_icon.pixmap(16, 16)
        self._error_indicator_label.setPixmap(self._error_indicator_pixmap)
        self._layout.addWidget(self._error_indicator_label, 0, Qt.AlignmentFlag.AlignVCenter)
        self._error_indicator_blink_timer = QTimer(self)
        self._error_indicator_blink_timer.setInterval(250)
        self._error_indicator_blink_timer.timeout.connect(
            lambda: self._error_indicator_label.setVisible(not self._error_indicator_label.isVisible())
        )
        self._error_indicator_idle_timer = QTimer(self)
        self._error_indicator_idle_timer.setSingleShot(True)
        self._error_indicator_idle_timer.setInterval(1000)
        self._error_indicator_idle_timer.timeout.connect(self._stop_error_indicator_blink)

    @property
    def input(self):
        return self._input

    def text(self):
        return self._input.text()

    def setText(self, value: str):
        self._input.setText(value)
        self._hide_error_indicator()

    def clear(self):
        self._input.clear()
        self._hide_error_indicator()

    def validator(self):
        return self._input.validator()

    def validate(self):
        validator = self.validator()
        if not validator:
            return QValidator.State.Acceptable
        state, _, _ = validator.validate(self.text(), 0)
        return state

    def _start_error_indicator_blink(self):
        self._error_indicator_label.setVisible(True)
        if not self._error_indicator_blink_timer.isActive():
            self._error_indicator_blink_timer.start()
        self._error_indicator_idle_timer.start()

    def _stop_error_indicator_blink(self):
        self._error_indicator_blink_timer.stop()
        self._error_indicator_idle_timer.stop()
        self._error_indicator_label.setVisible(True)

    def _hide_error_indicator(self):
        self._stop_error_indicator_blink()
        self._error_indicator_label.setVisible(False)

    def on_text_changed(self):
        if self.validate() != QValidator.State.Acceptable:
            self._start_error_indicator_blink()
        else:
            self._hide_error_indicator()

class ManageZoteroLibrariesWindow(QDialog):
    def __init__(self, libraries: list[ZoteroLibrary] | None = None):
        super().__init__()
        self.setWindowTitle("Manage Zotero Libraries - SourceUp")
        self.setFixedSize(1280, 720)
        self._model = ZoteroLibraryModel(libraries)
        self._root = QVBoxLayout(self)
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setSizes([1, 2])
        self._splitter.setStyleSheet("QSplitter::handle { background-color: #cccccc; }")
        self._list_panel_host = QWidget()
        self._list_panel = QVBoxLayout(self._list_panel_host)
        self._list_view = QListView()
        self._list_view.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self._list_view.setModel(self._model)
        self._list_view.selectionModel().currentChanged.connect(self._on_list_selection_changed)
        self._list_panel.addWidget(self._list_view)
        self._list_buttons_host = QWidget()
        self._list_buttons = QHBoxLayout(self._list_buttons_host)
        self._new_button = QPushButton("New")
        self._new_button.setDefault(False)
        self._new_button.setAutoDefault(False)
        self._new_button.clicked.connect(self._on_new_button_clicked)
        self._list_buttons.addWidget(self._new_button)
        self._delete_button = QPushButton("Delete")
        self._delete_button.setDefault(False)
        self._delete_button.setAutoDefault(False)
        self._delete_button.setDisabled(True)
        self._delete_button.clicked.connect(self._on_delete_button_clicked)
        self._list_buttons.addWidget(self._delete_button)
        self._delete_all_button = QPushButton("Delete all")
        self._delete_all_button.setDefault(False)
        self._delete_all_button.setAutoDefault(False)
        self._delete_all_button.setDisabled(True)
        self._delete_all_button.clicked.connect(self._on_delete_all_button_clicked)
        self._list_buttons.addWidget(self._delete_all_button)
        self._list_panel.addWidget(self._list_buttons_host)
        self._splitter.addWidget(self._list_panel_host)
        self._form_panel_host = QWidget()
        self._form_panel = QVBoxLayout(self._form_panel_host)
        self._form_host = QWidget()
        self._form = QFormLayout(self._form_host)
        self._library_type_combo = QComboBox()
        self._library_type_combo.currentIndexChanged.connect(self._on_library_type_combo_changed)
        self._form.addRow("Library Type", self._library_type_combo)
        self._library_id_input = QLineEdit()
        self._library_id_input.returnPressed.connect(self._on_save_button_clicked)
        self._validated_library_id_input = ValidatedLineEdit(
            self._library_id_input,
            QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9]+")
        ))
        self._form.addRow("Library ID", self._validated_library_id_input)
        self._library_id_help_label = QLabel()
        self._library_id_help_label.setTextFormat(Qt.TextFormat.RichText)
        self._library_id_help_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._library_id_help_label.setOpenExternalLinks(True)
        self._form.addRow("", self._library_id_help_label)
        self._private_access_checkbox = QCheckBox()
        self._private_access_checkbox.setChecked(False)
        self._private_access_checkbox.toggled.connect(self._on_private_access_checkbox_toggled)
        self._form.addRow("Private Access", self._private_access_checkbox)
        self._private_key_input_label = QLabel("Private Key")
        self._private_key_input_label.setVisible(self._private_access_checkbox.isChecked())
        self._private_key_input = QLineEdit()
        self._private_key_input.setVisible(self._private_access_checkbox.isChecked())
        self._private_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._private_key_input.setMaxLength(24)
        self._private_key_input.returnPressed.connect(self._on_save_button_clicked)
        self._validated_private_key_input = ValidatedLineEdit(
            self._private_key_input,
            QRegularExpressionValidator(QRegularExpression("[A-Za-z0-9]+")
        ))
        self._form.addRow(self._private_key_input_label, self._validated_private_key_input)
        self._private_key_help_label = QLabel(
            "You can create a new Private Key in your "
            "<a href='https://www.zotero.org/settings/keys'>Zotero account settings</a>"
        )
        self._private_key_help_label.setVisible(self._private_access_checkbox.isChecked())
        self._private_key_help_label.setTextFormat(Qt.TextFormat.RichText)
        self._private_key_help_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self._private_key_help_label.setOpenExternalLinks(True)
        self._form.addRow("", self._private_key_help_label)
        self._save_button = QPushButton("Save")
        self._save_button.clicked.connect(self._on_save_button_clicked)
        self._form.addRow("", self._save_button)
        self._form_panel.addWidget(self._form_host)
        self._splitter.addWidget(self._form_panel_host)
        self._root.addWidget(self._splitter)
        self._dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel) # type: ignore
        self._dialog_buttons.rejected.connect(self.close)
        self._dialog_buttons.accepted.connect(self.accept)
        self._root.addWidget(self._dialog_buttons)
        self._populate_library_type_combo()
        self._refresh_delete_enabled()
        self._refresh_delete_all_enabled()
        self._on_library_type_combo_changed()

    @property
    def libraries(self):
        return self._model.rows

    def _populate_library_type_combo(self):
        self._library_type_combo.clear()
        for library_type in LibraryType:
            self._library_type_combo.addItem(library_type.name.capitalize(), library_type)

    def _refresh_delete_enabled(self):
        self._delete_button.setEnabled(self._list_view.currentIndex().isValid())

    def _refresh_delete_all_enabled(self):
        self._delete_all_button.setEnabled(self._model.rowCount() > 0)

    def _clear_list_selection(self):
        self._list_view.clearFocus()
        self._list_view.clearSelection()
        self._list_view.setCurrentIndex(QModelIndex())
        self._refresh_delete_enabled()
        self._refresh_delete_all_enabled()

    def _select_list_idx(self, idx: QModelIndex):
        if idx.isValid():
            self._list_view.setCurrentIndex(idx)
            self._list_view.scrollTo(idx)
            self._refresh_delete_enabled()
            self._refresh_delete_all_enabled()

    def _clear_library_form(self):
        self._library_type_combo.setCurrentIndex(0)
        self._validated_library_id_input.input.setFocus()
        self._validated_library_id_input.clear()
        self._private_access_checkbox.setChecked(False)
        self._validated_private_key_input.clear()

    def _fill_library_form(self, library: ZoteroLibrary):
        self._library_type_combo.setCurrentIndex(self._library_type_combo.findData(library.library_type))
        self._validated_library_id_input.input.setFocus()
        self._validated_library_id_input.setText(library.library_id)
        self._private_access_checkbox.setChecked(bool(library.private_key))
        self._validated_private_key_input.setText(library.private_key)

    def _add_or_update_library(self, library: ZoteroLibrary):
        self._list_view.setFocus()
        idx = self._list_view.currentIndex()
        if idx.isValid():
            self._model.update_row(idx.row(), library)
            self._select_list_idx(idx)
        else:
            next_row = self._model.rowCount()
            self._model.add_row(library)
            new_idx = self._model.index(next_row)
            self._select_list_idx(new_idx)

    def _update_library_id_help_label(self):
        if self._library_type_combo.currentData() == LibraryType.USER:
            self._library_id_help_label.setText(
                "Copy your User Library ID from your "
                "<a href='https://www.zotero.org/settings/keys'>Zotero account settings</a>"
            )
        else:
            self._library_id_help_label.setText(
                "Copy the Group Library ID from your group's page in "
                "<a href='https://www.zotero.org/groups/'>Zotero groups</a>."
            )

    def _on_list_selection_changed(self, idx: QModelIndex, _: QModelIndex):
        self._clear_library_form()
        if idx.isValid():
            library = self._model.data(idx, Qt.ItemDataRole.UserRole)
            if library:
                self._fill_library_form(library)

    def _on_new_button_clicked(self):
        self._clear_list_selection()
        self._clear_library_form()

    def _on_delete_button_clicked(self):
        if QMessageBox.question(self, "Delete", "Delete this library? This action cannot be undone.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            idx = self._list_view.currentIndex()
            if idx.isValid():
                self._model.remove_row(idx.row())
                self._clear_list_selection()
                self._clear_library_form()

    def _on_delete_all_button_clicked(self):
        if QMessageBox.question(self, "Delete all", "Delete all libraries? This action cannot be undone.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self._model.reset_rows()
            self._clear_list_selection()
            self._clear_library_form()

    def _on_library_type_combo_changed(self):
        self._update_library_id_help_label()

    def _on_private_access_checkbox_toggled(self):
        is_private = self._private_access_checkbox.isChecked()
        self._private_key_input_label.setVisible(is_private)
        self._private_key_input.setVisible(is_private)
        self._private_key_help_label.setVisible(is_private)
        if not is_private:
            self._validated_private_key_input.clear()

    def _on_save_button_clicked(self):
        if self._validated_library_id_input.validate() != QValidator.State.Acceptable:
            self._validated_library_id_input.input.setFocus()
            QMessageBox.critical(self, "Missing Library ID", "Please provide a Library ID.")
            return
        need_private_key = self._private_access_checkbox.isChecked()
        if need_private_key and self._validated_private_key_input.validate() != QValidator.State.Acceptable:
            self._validated_private_key_input.input.setFocus()
            QMessageBox.critical(self, "Missing Private Key", "Please provide a Private Key.")
            return
        library_type = self._library_type_combo.currentData()
        library_id = self._library_id_input.text().strip()
        private_key = self._private_key_input.text().strip()
        self._add_or_update_library(ZoteroLibrary(
            library_type,
            library_id,
            private_key if need_private_key else None,
        ))

