from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt

from sourceup.data.zotero_collection import ZoteroCollection


class ZoteroCollectionStorage:
    def __init__(self, data: list[ZoteroCollection] | None = None):
        self._data: list[ZoteroCollection] = data or []

    def count(self):
        return len(self._data or [])

    def all(self):
        return list(self._data or [])

    def at(self, row: int):
        if self.in_bounds(row):
            return self._data[row]
        return None

    def fill(self, data: list[ZoteroCollection] | None):
        self._data = data or []

    def in_bounds(self, row: int):
        return 0 <= row < self.count()

class ZoteroCollectionModel(QAbstractListModel):
    def __init__(self, rows: list[ZoteroCollection] | None = None):
        super().__init__()
        self._storage = ZoteroCollectionStorage(rows)

    @property
    def rows(self) -> list[ZoteroCollection]:
        return self._storage.all()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self._storage.count()

    def _is_valid_idx(self, idx: QModelIndex):
        return idx.isValid() and self._storage.in_bounds(idx.row())

    def data(self, idx: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if self._is_valid_idx(idx):
            collection = self._storage.at(idx.row())
            if role is Qt.ItemDataRole.UserRole: return collection
            if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
                return repr(collection)
        return None

    def flags(self, idx: QModelIndex):
        if self._is_valid_idx(idx):
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable  # type: ignore
        return Qt.ItemFlag.NoItemFlags

    def set_rows(self, rows: list[ZoteroCollection]):
        self.beginResetModel()
        self._storage.fill(rows)
        self.endResetModel()

    def at_row(self, row: int) -> ZoteroCollection:
        return self._storage.at(row)
