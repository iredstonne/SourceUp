from pathlib import Path
from typing import Optional, List, Iterable
from PySide6.QtCore import QModelIndex, QSignalBlocker, QAbstractListModel
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QListView,
    QSplitter, QMessageBox, QDialog, QSizePolicy, QFileDialog, QLabel
)
from sourceup.client.zotero_functions import fetch_collections, fetch_collection_items, fetch_items, decipher_client_error
from sourceup.exporter.wordbibxml_functions import decipher_bibxml_export_error, export_as_bibxml_to_output_file
from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.collection.ZoteroCollection import ZoteroCollection
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.library.ZoteroLibraryType import ZoteroLibraryType
from sourceup.settings.Settings import Settings
from sourceup.settings.data.ZoteroLibraryData import ZoteroLibraryData
from sourceup.ui.model.ZoteroCollectionListModel import ZoteroCollectionListModel
from sourceup.ui.model.ZoteroItemListModel import ZoteroItemListModel
from sourceup.ui.background.BackgroundJobRunner import BackgroundJobRunner
from sourceup.ui.background.ZoteroLibraryFetchDialogBackgroundJobPresentation import (
    ZoteroLibraryFetchDialogBackgroundJobPresentation
)
from sourceup.ui.background.WordBibXMLExportDialogBackgroundJobPresentation import (
    WordBibXMLExportDialogBackgroundJobPresentation
)
from sourceup.ui.window.ZoteroManageLibrariesDialog import ZoteroManageLibrariesDialog
from sourceup.ui.widget.ZoteroItemDataPreviewWidget import ZoteroItemDataPreviewWidget

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle(f"{app.applicationName()} {app.applicationVersion()}")
        self.resize(1280, 720)
        self._settings = Settings(Path.cwd() / ".sourceup" / "settings.json")
        self._settings_data = self._settings.load()
        self._libraries: list[ZoteroLibrary] = [
            ZoteroLibrary(
                library_type=ZoteroLibraryType.__members__.get(library.library_type, ZoteroLibraryType.USER),
                library_id=library.library_id or "",
                private_key=library.private_key or "",
            )
            for library in self._settings_data.libraries
        ]
        self._selected_library: Optional[ZoteroLibrary] = None
        self._collection_list_model = ZoteroCollectionListModel()
        self._collection_item_list_model = ZoteroItemListModel()
        self._library_fetch_background_job_runner = BackgroundJobRunner(
            self,
            ZoteroLibraryFetchDialogBackgroundJobPresentation()
        )
        self._word_bibxml_export_background_job_runner = BackgroundJobRunner(
            self,
            WordBibXMLExportDialogBackgroundJobPresentation()
        )
        self._build_root()
        self._populate_library_combo()

    def _build_root(self):
        _root_host = QWidget()
        _root_layout = QVBoxLayout(_root_host)
        _root_layout.addWidget(self._build_toolbar_host())
        _root_layout.addWidget(self._build_splitter_host())
        self.setCentralWidget(_root_host)

    def _build_toolbar_host(self) -> QWidget:
        _toolbar_host = QWidget()
        _toolbar_layout = QHBoxLayout(_toolbar_host)
        _toolbar_layout.addWidget(self._build_library_combo())
        _toolbar_layout.addWidget(self._build_refresh_button())
        _toolbar_layout.addWidget(self._build_export_items_as_word_bibxml_button())
        _toolbar_layout.addStretch()
        _toolbar_layout.addWidget(self._build_manage_libraries_button())
        return _toolbar_host

    def _build_library_combo(self) -> QComboBox:
        self._library_combo = QComboBox()
        self._library_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._library_combo.setPlaceholderText("(empty)")
        self._library_combo.setToolTip("Choose a Zotero Library")
        self._library_combo.currentIndexChanged.connect(self._on_library_combo_changed)
        return self._library_combo

    def _build_refresh_button(self) -> QPushButton:
        _refresh_button = QPushButton("Refresh")
        _refresh_button.setToolTip("Refresh")
        _refresh_button.clicked.connect(self._on_refresh_button_click)
        return _refresh_button

    def _build_export_items_as_word_bibxml_button(self) -> QPushButton:
        _export_items_as_bibxml_button = QPushButton("Export selected item(s) as Word BibXML")
        _export_items_as_bibxml_button.setToolTip("Export items as Word BibXML")
        _export_items_as_bibxml_button.clicked.connect(self._on_export_collection_items_as_word_bibxml_button_click)
        return _export_items_as_bibxml_button

    def _build_manage_libraries_button(self) -> QPushButton:
        _manage_libraries_button = QPushButton("Manage Zotero Libraries...")
        _manage_libraries_button.clicked.connect(self._on_manage_libraries_button_click)
        return _manage_libraries_button

    @staticmethod
    def _wrap_header_host_with_list_view(
        _header_host: QWidget,
        _list_view: QListView
    ) -> QWidget:
        _host = QWidget()
        _layout = QVBoxLayout(_host)
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.addWidget(_header_host, 0)
        _layout.addWidget(_list_view, 1)
        return _host

    @staticmethod
    def _create_list_view(
        _list_model: QAbstractListModel,
        _on_changed_slot: object
    ) -> QListView:
        _list_view = QListView()
        _list_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        _list_view.setModel(_list_model)
        _list_view.clicked.connect(_on_changed_slot)
        return _list_view

    def _build_collection_list_view(self) -> QListView:
        self._collection_list_view = self._create_list_view(
            self._collection_list_model,
            self._on_collection_list_view_selection_model_changed
        )
        self._collection_list_view.setSelectionMode(QListView.SelectionMode.SingleSelection)
        return self._collection_list_view

    def _build_my_library_button(self) -> QPushButton:
        self._my_library_button = QPushButton("My Library")
        self._my_library_button.setToolTip("Show all items in the current library")
        self._my_library_button.setEnabled(bool(self._libraries))
        self._my_library_button.clicked.connect(self._on_my_library_button_clicked)
        return self._my_library_button

    def _wrap_header_host_with_collection_list_view(self):
        _header_host = QWidget()
        _header_layout = QHBoxLayout(_header_host)
        _header_layout.setContentsMargins(0, 0, 0, 0)
        _header_layout.addWidget(QLabel("Collections"))
        _header_layout.addWidget(self._build_my_library_button())
        return self._wrap_header_host_with_list_view(_header_host, self._build_collection_list_view())

    def _build_collection_item_list_view(self) -> QListView:
        self._collection_item_list_view = self._create_list_view(
            self._collection_item_list_model,
            self._on_collection_item_list_view_selection_model_changed
        )
        self._collection_item_list_view.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        return self._collection_item_list_view

    def _build_collection_item_data_preview(self):
        self._collection_item_data_preview = ZoteroItemDataPreviewWidget()
        self._refresh_collection_item_data_preview()
        return self._collection_item_data_preview

    def _build_splitter_host(self) -> QSplitter:
        _splitter_a_host = QSplitter()
        _splitter_a_host.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        _splitter_a_host.setStyleSheet("QSplitter::handle { background-color: #cccccc; }")
        _splitter_a_host.addWidget(self._wrap_header_host_with_collection_list_view())
        _splitter_b_host = QSplitter()
        _splitter_b_host.addWidget(self._build_collection_item_list_view())
        _splitter_b_host.addWidget(self._build_collection_item_data_preview())
        _splitter_b_host.setStretchFactor(0, 1)
        _splitter_b_host.setStretchFactor(1, 3)
        _splitter_a_host.addWidget(_splitter_b_host)
        _splitter_a_host.setStretchFactor(0, 1)
        _splitter_a_host.setStretchFactor(1, 4)
        return _splitter_a_host

    def closeEvent(self, event):
        self._settings.dispose()
        super().closeEvent(event)

    def _get_selected_collection(self) -> Optional[ZoteroCollection]:
        _collection_list_view_selection_model = self._collection_list_view.selectionModel()
        if _collection_list_view_selection_model is None:
            return None
        _collection_list_view_selection_model_current_index = _collection_list_view_selection_model.currentIndex()
        if not _collection_list_view_selection_model_current_index.isValid():
            return None
        return self._collection_list_model.row_item_at(_collection_list_view_selection_model_current_index.row())

    def _get_selected_collection_item(self) -> Optional[ZoteroItem]:
        _collection_item_list_view_selection_model = self._collection_item_list_view.selectionModel()
        if _collection_item_list_view_selection_model is None:
            return None
        _collection_item_list_view_selection_model_current_index = _collection_item_list_view_selection_model.currentIndex()
        if not _collection_item_list_view_selection_model_current_index.isValid():
            return None
        return self._collection_item_list_model.row_item_at(_collection_item_list_view_selection_model_current_index.row())

    def _get_selected_collection_items(self) -> Iterable[ZoteroItem]:
        _collection_item_list_view_selection_model = self._collection_item_list_view.selectionModel()
        if _collection_item_list_view_selection_model is None:
            return []
        _collection_item_list_view_selection_model_selected_indexes = _collection_item_list_view_selection_model.selectedIndexes()
        return [
            self._collection_item_list_model.row_item_at(_collection_item_list_view_selection_model_selected_index.row())
            for _collection_item_list_view_selection_model_selected_index in _collection_item_list_view_selection_model_selected_indexes
            if _collection_item_list_view_selection_model_selected_index.isValid()
        ]

    def _refresh_collection_item_data_preview(self):
        _selected_collection_item = self._get_selected_collection_item()
        self._collection_item_data_preview.preview(_selected_collection_item)
        self._collection_item_data_preview.setVisible(bool(_selected_collection_item))

    def _on_fetch_collection_items_worker_fn_finished(self, _fetched_collection_item_rows: Iterable[ZoteroItem]):
        self._collection_item_list_model.set_rows(_fetched_collection_item_rows)
        self._collection_item_list_view.clearSelection()
        self._collection_item_list_view.setFocus()
        self._refresh_collection_item_data_preview()

    def _on_fetch_collection_items_worker_fn_error(self, e: Exception):
        QMessageBox.critical(self, "Zotero",
         "Failed to fetch collection items from Zotero:\n\n"
         f"{decipher_client_error(e)}"
        )

    def _refresh_collection_items(self):
        _selected_library = self._selected_library
        _selected_collection = self._get_selected_collection()
        if not _selected_library or not _selected_collection:
            self._collection_item_list_model.clear_rows()
            self._collection_item_list_view.clearFocus()
            self._refresh_collection_item_data_preview()
            return
        self._library_fetch_background_job_runner.run(
            fetch_collection_items,
            self._on_fetch_collection_items_worker_fn_finished,
            self._on_fetch_collection_items_worker_fn_error,
            _selected_library, _selected_collection
        )

    def _on_fetch_collections_worker_fn_finished(self, _fetched_collection_rows: Iterable[ZoteroCollection]):
        self._collection_list_model.set_rows(_fetched_collection_rows)
        self._collection_list_view.clearSelection()
        self._collection_list_view.setFocus()
        self._collection_item_list_model.clear_rows()
        self._collection_item_list_view.clearFocus()
        self._refresh_collection_item_data_preview()

    def _on_fetch_collections_worker_fn_error(self, e: Exception):
        QMessageBox.critical(self, "Zotero", (
            "Failed to fetch collections from Zotero:\n\n"
            f"{decipher_client_error(e)}"
        ))

    def _refresh_collections(self):
        _selected_library = self._selected_library
        if not _selected_library:
            self._collection_list_model.clear_rows()
            self._collection_list_view.clearFocus()
            self._collection_item_list_model.clear_rows()
            self._collection_item_list_view.clearFocus()
            self._refresh_collection_item_data_preview()
            return
        self._library_fetch_background_job_runner.run(
            fetch_collections,
            self._on_fetch_collections_worker_fn_finished,
            self._on_fetch_collections_worker_fn_error,
            _selected_library
        )

    def _on_collection_item_list_view_selection_model_changed(self, _current_idx: QModelIndex):
        self._refresh_collection_item_data_preview()

    def _on_collection_list_view_selection_model_changed(self, _current_idx: QModelIndex):
        _collection_item_list_view_selection_model = self._collection_item_list_view.selectionModel()
        if _collection_item_list_view_selection_model is not None:
            with QSignalBlocker(_collection_item_list_view_selection_model):
                self._refresh_collection_items()

    def _on_library_combo_changed(self, _index: int):
        self._selected_library = self._library_combo.itemData(_index)
        _collection_list_view_selection_model = self._collection_list_view.selectionModel()
        if _collection_list_view_selection_model is not None:
            with QSignalBlocker(_collection_list_view_selection_model):
                self._refresh_collections()

    def _on_refresh_button_click(self):
        _selected_library = self._selected_library
        if not _selected_library:
            QMessageBox.information(self, "No library", "Please choose a library first before refreshing.")
            return
        self._refresh_collections()

    def _on_export_collection_items_as_word_bibxml_worker_fn_finished(self, _output_file_save_path: str):
        QMessageBox.information(self, "Word BibXML", (
            "Export to Word BibXML completed.\n\n"
            f"Saved to:\n{_output_file_save_path}"
        ))

    def _on_export_collection_items_as_word_bibxml_worker_fn_error(self, e: Exception):
        QMessageBox.critical(self, "Word BibXML", (
            "Failed to export as Word BibXML:\n\n"
            f"{decipher_bibxml_export_error(e)}"
        ))

    def _export_collection_items(self):
        _selected_collection_items = self._get_selected_collection_items()
        if not _selected_collection_items:
            QMessageBox.information(self, "No collection items","Please choose at least one collection item before exporting as Word BibXML.")
            return
        _output_file_save_dialog = QFileDialog(self)
        _output_file_save_dialog.setWindowTitle("Export Word BibXML as ...")
        _output_file_save_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        _output_file_save_dialog.setNameFilter("Word BibXML (*.xml)")
        _output_file_save_dialog.setDefaultSuffix(".xml")

        if _output_file_save_dialog.exec() != QFileDialog.DialogCode.Accepted:
            return
        _output_file_save_path = _output_file_save_dialog.selectedFiles()[0]

        self._word_bibxml_export_background_job_runner.run(
            export_as_bibxml_to_output_file,
            self._on_export_collection_items_as_word_bibxml_worker_fn_finished,
            self._on_export_collection_items_as_word_bibxml_worker_fn_error,
            _selected_collection_items, _output_file_save_path
        )

    def _on_export_collection_items_as_word_bibxml_button_click(self):
        _selected_library = self._selected_library
        if not _selected_library:
            QMessageBox.information(self, "No library", "Please choose a library first before exporting as Word BibXML.")
            return
        _selected_collection = self._get_selected_collection()
        if not _selected_collection:
            QMessageBox.information(self, "No collection", "Please choose a collection first before exporting as Word BibXML.")
            return
        self._export_collection_items()

    def _on_fetch_my_library_items_worker_fn_finished(self, _fetched_my_library_items_rows: Iterable[ZoteroItem]):
        self._collection_item_list_model.set_rows(_fetched_my_library_items_rows)
        self._collection_list_view.clearSelection()
        self._collection_list_view.setCurrentIndex(QModelIndex())
        self._collection_item_list_view.clearSelection()
        self._collection_item_list_view.setCurrentIndex(QModelIndex())
        self._collection_item_list_view.setFocus()
        self._refresh_collection_item_data_preview()

    def _on_fetch_my_library_items_worker_fn_error(self, e: Exception):
        QMessageBox.critical(self, "Zotero", (
            "Failed to fetch items from Zotero:\n\n"
            f"{decipher_client_error(e)}"
        ))

    def _on_my_library_button_clicked(self):
        _selected_library = self._selected_library
        if not _selected_library:
            return
        self._collection_list_view.clearSelection()
        self._collection_list_view.setCurrentIndex(QModelIndex())
        self._library_fetch_background_job_runner.run(
            fetch_items,
            self._on_fetch_my_library_items_worker_fn_finished,
            self._on_fetch_my_library_items_worker_fn_error,
            _selected_library
        )

    def _populate_library_combo(self):
        self._library_combo.clear()
        for _library in self._libraries:
            self._library_combo.addItem(str(_library), _library)
        if self._libraries:
            self._library_combo.setCurrentIndex(0)
            self._my_library_button.setEnabled(True)
        else:
            self._my_library_button.setEnabled(False)

    def _on_manage_libraries_button_click(self):
        dialog = ZoteroManageLibrariesDialog(self._libraries, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._libraries = dialog.libraries
            self._populate_library_combo()
            self._settings_data.libraries = [
                ZoteroLibraryData(
                    library_type=library.library_type or "",
                    library_id=library.library_id or "",
                    private_key=library.private_key or ""
                )
                for library in self._libraries
            ]
            self._settings.save(self._settings_data)

    @property
    def libraries(self) -> List[ZoteroLibrary]:
        return self._libraries
