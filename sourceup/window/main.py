import datetime
import traceback

from lxml import etree

from PySide6.QtCore import Qt, QModelIndex, QThread, QObject, Signal
from PySide6.QtWidgets import QMainWindow, QPushButton, QDialog, QComboBox, QLabel, QWidget, QHBoxLayout, \
    QVBoxLayout, QMessageBox, QSplitter, QListView, QTableView, QSizePolicy, QProgressBar, \
    QFileDialog, QHeaderView

from sourceup.client.zotero_client import fetch_collections, fetch_items_from_collection
from sourceup.data.zotero_collection import ZoteroCollection
from sourceup.data.zotero_library import ZoteroLibrary
from sourceup.model.zotero_collection_model import ZoteroCollectionModel
from sourceup.model.zotero_item_model import ZoteroItemModel
from sourceup.window.manage_zotero_libraries import ManageZoteroLibrariesWindow

class FetcherWorker(QObject):
    finished = Signal(object)
    error = Signal(Exception)

    def __init__(self, fn, *args):
        super().__init__()
        self._fn = fn
        self._args = args

    def run(self):
        try:
            self.finished.emit(self._fn(*self._args))
        except Exception as e:
            self.error.emit(e)


B_NS = "http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
nsmap = {"b": B_NS}


def _generate_title_node(b_source, title: str):
    if title:
        etree.SubElement(b_source, "{%s}Title" % B_NS).text = title

def _generate_creators_node(b_source, creator_names: list[str]):
    b_author = etree.SubElement(b_source, "{%s}Author" % B_NS)
    b_namelist = etree.SubElement(b_author, "{%s}NameList" % B_NS)

    if len(creator_names) == 0:
        return

    for creator_name in creator_names:
        creator_name = (creator_name or "").strip()
        if not creator_name:
            continue
        if "," in creator_name:
            tokens = [token.strip() for token in creator_name.split(",", 1)]
            first = tokens[0]
            last = tokens[1] if len(tokens) > 1 else ""
        else:
            tokens = creator_name.split(" ", 1)
            first = tokens[0]
            last = tokens[1] if len(tokens) > 1 else ""

        b_person = etree.SubElement(b_namelist, "{%s}Person" % B_NS)
        etree.SubElement(b_person, "{%s}First" % B_NS).text = first
        etree.SubElement(b_person, "{%s}Last" % B_NS).text = last


def _generate_date_node(b_source, date: str):
    year = None
    month = None
    day = None
    try:
        dt = datetime.datetime.fromisoformat(date.replace("Z", "+00:00"))
        year, month, day = dt.year, dt.month, dt.day
    except:
        try:
            dt = datetime.datetime.strptime(date, "%Y-%m-%d")
            year, month, day = dt.year, dt.month, dt.day
        except:
            try:
                dt = datetime.datetime.strptime(date, "%Y")
                year = dt.year
            except:
                print(f"Failed to parse date: {date}")
                return

    if year: etree.SubElement(b_source, "{%s}Year" % B_NS).text = str(year)
    if month: etree.SubElement(b_source, "{%s}Month" % B_NS).text = str(month)
    if day: etree.SubElement(b_source, "{%s}Day" % B_NS).text = str(day)

def _generate_link_node(b_source, link: str):
    if link:
        etree.SubElement(b_source, "{%s}URL" % B_NS).text = link

class FetcherDialog(QWidget):
    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        self.setContentsMargins(8, 8, 8, 8)
        self._layout = QVBoxLayout(self)
        self._label = QLabel(text, self)
        self._layout.addWidget(self._label)
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setFixedWidth(self.width())
        self._progress_bar.setRange(0, 0)
        self._progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._layout.addWidget(self._progress_bar)
        self.setLayout(self._layout)
        self.adjustSize()
        self.setFixedSize(self.size())
        self.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SourceUp")
        self.resize(1280, 720)
        self.collection_model = ZoteroCollectionModel()
        self.item_model = ZoteroItemModel()
        self._librairies: list[ZoteroLibrary] = []
        self._current_library: ZoteroLibrary | None = None
        self._root_host = QWidget()
        self._root = QVBoxLayout(self._root_host)
        self._toolbar = QHBoxLayout()
        self._toolbar.addWidget(QLabel("Library:"))
        self._library_combo = QComboBox()
        self._library_combo.setPlaceholderText("(no library selected)")
        self._library_combo.setMinimumWidth(300)
        self._library_combo.currentIndexChanged.connect(self._on_library_combo_changed)
        self._toolbar.addWidget(self._library_combo)
        self._manage_libraries_button = QPushButton("Manage...", self)
        self._manage_libraries_button.clicked.connect(self._on_manage_libraries_button_click)
        self._toolbar.addWidget(self._manage_libraries_button)
        self._refresh_current_library_button = QPushButton("Refresh", self)
        self._refresh_current_library_button.clicked.connect(self._on_refresh_library_button_click)
        self._toolbar.addWidget(self._refresh_current_library_button)
        self._export_button = QPushButton("Export collection to Word BibXML (Work in progress, not fully supported)", self)
        self._export_button.clicked.connect(self._on_export_button_click)
        self._toolbar.addWidget(self._export_button)
        self._toolbar.addStretch(1)
        self._root.addLayout(self._toolbar)
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setStyleSheet("QSplitter::handle { background-color: #cccccc; }")
        self._collections_list_view = QListView()
        self._collections_list_view.setModel(self.collection_model)
        self._collections_list_view.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self._collections_list_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self._collections_list_view.selectionModel().currentChanged.connect(self._on_collection_list_changed)
        self._splitter.addWidget(self._collections_list_view)
        self._items_table_view = QTableView()
        self._items_table_view.setModel(self.item_model)
        self._items_table_view.setTextElideMode(Qt.TextElideMode.ElideRight)
        self._items_table_view.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self._items_table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._items_table_view.setSelectionMode(QListView.SelectionMode.MultiSelection)
        self._items_table_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)
        self._splitter.addWidget(self._items_table_view)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 2)
        self._root.addWidget(self._splitter)
        self.setCentralWidget(self._root_host)


    def _refresh_collections_in_library(self, library: ZoteroLibrary):
        self.item_model.set_rows([])
        self.collection_model.set_rows([])
        self._collections_list_view.clearFocus()
        self._collections_list_view.clearSelection()
        self._collections_fetcher_dialog = FetcherDialog("Zotero", "Fetching collections from Zotero…")
        self._collections_fetcher_thread = QThread(self)
        self._collections_fetcher_worker = FetcherWorker(fetch_collections, library)
        self._collections_fetcher_worker.moveToThread(self._collections_fetcher_thread)
        self._collections_fetcher_thread.started.connect(self._collections_fetcher_worker.run)
        self._collections_fetcher_worker.finished.connect(self._on_collections_ready)
        self._collections_fetcher_worker.finished.connect(self._collections_fetcher_thread.quit)
        self._collections_fetcher_worker.finished.connect(self._collections_fetcher_dialog.close)
        self._collections_fetcher_worker.finished.connect(self._collections_fetcher_worker.deleteLater)
        self._collections_fetcher_worker.finished.connect(self._collections_fetcher_thread.deleteLater)
        self._collections_fetcher_worker.finished.connect(self._collections_fetcher_dialog.deleteLater)
        self._collections_fetcher_worker.error.connect(self._on_collections_error)
        self._collections_fetcher_worker.error.connect(self._collections_fetcher_thread.quit)
        self._collections_fetcher_worker.error.connect(self._collections_fetcher_dialog.close)
        self._collections_fetcher_worker.error.connect(self._collections_fetcher_worker.deleteLater)
        self._collections_fetcher_worker.error.connect(self._collections_fetcher_thread.deleteLater)
        self._collections_fetcher_worker.error.connect(self._collections_fetcher_dialog.deleteLater)
        self._collections_fetcher_thread.start()

    def _refresh_items_from_collection_in_library(self, library: ZoteroLibrary, collection: ZoteroCollection):
        self.item_model.set_rows([])
        self._items_table_view.clearFocus()
        self._items_table_view.clearSelection()
        self._items_fetcher_dialog = FetcherDialog("Zotero", "Fetching items from Zotero…")
        self._items_fetcher_thread = QThread(self)
        self._items_fetcher_worker = FetcherWorker(fetch_items_from_collection, library, collection)
        self._items_fetcher_worker.moveToThread(self._items_fetcher_thread)
        self._items_fetcher_thread.started.connect(self._items_fetcher_worker.run)
        self._items_fetcher_worker.finished.connect(self._on_items_ready)
        self._items_fetcher_worker.finished.connect(self._items_fetcher_thread.quit)
        self._items_fetcher_worker.finished.connect(self._items_fetcher_dialog.close)
        self._items_fetcher_worker.finished.connect(self._items_fetcher_worker.deleteLater)
        self._items_fetcher_worker.finished.connect(self._items_fetcher_thread.deleteLater)
        self._items_fetcher_worker.finished.connect(self._items_fetcher_dialog.deleteLater)
        self._items_fetcher_worker.error.connect(self._on_items_error)
        self._items_fetcher_worker.error.connect(self._items_fetcher_thread.quit)
        self._items_fetcher_worker.error.connect(self._items_fetcher_dialog.close)
        self._items_fetcher_worker.error.connect(self._items_fetcher_worker.deleteLater)
        self._items_fetcher_worker.error.connect(self._items_fetcher_thread.deleteLater)
        self._items_fetcher_worker.error.connect(self._items_fetcher_dialog.deleteLater)
        self._items_fetcher_thread.start()


    def _export_all_items_from_collection(self, library: ZoteroLibrary, collection: ZoteroCollection):
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path, _ =  QFileDialog.getSaveFileName(self,
            "Export collection to...",
            f"bib-{library.library_id}-{collection.key}-export-{timestamp}.xml",
              "Word BibXML (*.xml)"
        )
        if not path:
            return

        try:
            b_root = etree.Element("{%s}Sources" % B_NS, nsmap=nsmap)
            for item in self.item_model.rows:
                key = (getattr(item, "key") or "").strip()
                title = (getattr(item, "title") or "").strip()
                creator_names = (getattr(item, "creator_names") or [])
                date = (getattr(item, "date") or "").strip()
                link = (getattr(item, "link") or "").strip()

                b_source = etree.SubElement(b_root, "{%s}Source" % B_NS)
                etree.SubElement(b_source, "{%s}Tag" % B_NS).text = key
                etree.SubElement(b_source, "{%s}SourceType" % B_NS).text = "ElectronicSource" # TODO: map zotero item type to wordxml source type
                _generate_title_node(b_source, title)
                _generate_creators_node(b_source, creator_names)
                _generate_date_node(b_source, date)
                _generate_link_node(b_source, link)
            b_tree = etree.ElementTree(b_root)
            b_tree.write(path, encoding="utf-8", xml_declaration=True, pretty_print=True)
            QMessageBox.information(self, "Export library", "Exporting to Word BibXML done.")
        except etree.SerialisationError as e:
            QMessageBox.critical(self, "Export library", f"Couldn't serialize items to Word BibXML: \n {str(e)}")
        except OSError as e:
            QMessageBox.critical(self, "Export library", f"Couldn't write Word BibXML file:\n {str(e)}.")

    def _populate_libraries_combo(self):
        self._library_combo.clear()
        for library in self.librairies:
            self._library_combo.addItem(repr(library), library)
        if self.librairies:
            self._library_combo.setCurrentIndex(0)
        else:
            self.item_model.set_rows([])
            self.collection_model.set_rows([])

    def _on_manage_libraries_button_click(self):
        dialog = ManageZoteroLibrariesWindow(self._librairies, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.librairies = dialog.libraries
            self._populate_libraries_combo()

    def _on_library_combo_changed(self, current: int):
        library = self._library_combo.itemData(current)
        if not library:
            self.collection_model.set_rows([])
            self.item_model.set_rows([])
            return
        self._refresh_collections_in_library(library)

    def _on_refresh_library_button_click(self):
        library = self._library_combo.currentData()
        if not library:
            QMessageBox.information(self, "No library selected", "Please select a library first.")
            return
        self._refresh_collections_in_library(library)

    def _on_export_button_click(self):
        library = self._library_combo.currentData()
        if not library:
            QMessageBox.information(self, "No library selected", "Please select a library first.")
            return
        idx = self._collections_list_view.currentIndex()
        if not idx.isValid():
            QMessageBox.information(self, "No collection selected", "Please select a collection first.")
            return
        collection = self.collection_model.at_row(idx.row())
        self._export_all_items_from_collection(library, collection)

    def _on_collection_list_changed(self, current: QModelIndex, _: QModelIndex):
        library = self._library_combo.currentData()
        if not library:
            QMessageBox.information(self, "No library selected", "Please select a library first.")
            return
        if not current.isValid():
            self.item_model.set_rows([])
            return
        collection = self.collection_model.at_row(current.row())
        self._refresh_items_from_collection_in_library(library, collection)

    def _on_collections_ready(self, rows):
        self.collection_model.set_rows(rows)

    def _on_items_ready(self, rows):
        self.item_model.set_rows(rows)
        items_table_header = self._items_table_view.horizontalHeader()
        items_table_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._items_table_view.resizeColumnsToContents()

    def _on_collections_error(self, e: Exception):
        print({"".join(traceback.format_exception(type(e), e, e.__traceback__))})
        QMessageBox.critical(self, "Zotero", f"Failed to fetch collections from Zotero: \n{str(e)}")

    def _on_items_error(self, e: Exception):
        print({"".join(traceback.format_exception(type(e), e, e.__traceback__))})
        QMessageBox.critical(self, "Zotero", f"Failed to fetch items from Zotero: \n{str(e)}")

