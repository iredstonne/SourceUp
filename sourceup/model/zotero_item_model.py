from typing import List, Tuple, Callable, Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from sourceup.data.zotero_item import ZoteroItem


class ZoteroItemStorage:
    def __init__(self, data: list[ZoteroItem] | None = None):
        self._data: list[ZoteroItem] = data or []

    def count(self):
        return len(self._data or [])

    def all(self):
        return list(self._data or [])

    def at(self, row: int):
        if self.in_bounds(row):
            return self._data[row]
        return None

    def fill(self, data: list[ZoteroItem] | None):
        self._data = data or []

    def in_bounds(self, row: int):
        return 0 <= row < self.count()


class ZoteroItemModel(QAbstractTableModel):
    def __init__(self, rows: list[ZoteroItem] | None = None):
        super().__init__()
        self._static_columns: List[Tuple[str, Callable[[ZoteroItem | None], Any]]] = [
            ("Title", lambda item: item.title),
            ("Creator", lambda item: ", ".join(item.creator_names)),
            ("Date", lambda item: item.date or "n.d."),
            ("Link", lambda item: item.link)
        ]
        self._storage = ZoteroItemStorage(rows)

    @property
    def rows(self) -> list[ZoteroItem]:
        return self._storage.all()

    def columnCount(self, _: QModelIndex = QModelIndex()) -> int:
        return len(self._static_columns)

    def rowCount(self, _: QModelIndex = QModelIndex()) -> int:
        return self._storage.count()

    def _is_valid_idx(self, idx: QModelIndex):
        return idx.isValid() and self._storage.in_bounds(idx.row())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            key = self._static_columns[section][0]
            return key
        return None

    def data(self, idx: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if self._is_valid_idx(idx):
            item = self._storage.at(idx.row())
            if role is Qt.ItemDataRole.UserRole: return item
            if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
                accessor = self._static_columns[idx.column()][1]
                return accessor(item)
        return None

    def flags(self, idx: QModelIndex):
        if self._is_valid_idx(idx):
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable  # type: ignore
        return Qt.ItemFlag.NoItemFlags

    #def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder):
    #    static_column = self._static_columns[column]
    #    if static_column:
    #        key = static_column[0]
    #        self.layoutAboutToBeChanged.emit()
    #        #self._storage.sort(key, reverse=order == Qt.SortOrder.DescendingOrder)
    #        self.layoutChanged.emit()

    def set_rows(self, rows: list[ZoteroItem]):
        self.beginResetModel()
        self._storage.fill(rows)
        self.endResetModel()

    def at_row(self, row: int) -> ZoteroItem:
        return self._storage.at(row)
