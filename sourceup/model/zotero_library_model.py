from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex

from sourceup.data.zotero_library import ZoteroLibrary


class ZoteroLibraryStorage:
    def __init__(self, data: list[ZoteroLibrary] | None = None):
        self._data: list[ZoteroLibrary] = data or []

    def count(self):
        return len(self._data or [])

    def all(self):
        return list(self._data or [])

    def pop_all(self):
        self._data = []

    def push(self, value: ZoteroLibrary):
        self._data.append(value)

    def pop(self, row: int):
        if self.in_bounds(row):
            self._data.pop(row)

    def mutate(self, row: int, value: ZoteroLibrary):
        if self.in_bounds(row):
            self._data[row] = value

    def at(self, row: int):
        if self.in_bounds(row):
            return self._data[row]
        return None

    def in_bounds(self, row: int):
        return 0 <= row < self.count()

class ZoteroLibraryModel(QAbstractListModel):
    def __init__(self, rows: list[ZoteroLibrary] | None = None):
        super().__init__()
        self._storage = ZoteroLibraryStorage(rows)

    @property
    def rows(self) -> list[ZoteroLibrary]:
        return self._storage.all()

    def rowCount(self, _: QModelIndex = QModelIndex()) -> int:
        return self._storage.count()

    def _is_valid_idx(self, idx: QModelIndex):
        return idx.isValid() and self._storage.in_bounds(idx.row())

    def data(self, idx: QModelIndex = QModelIndex(), role: int = Qt.ItemDataRole.UserRole):
        if self._is_valid_idx(idx):
            library = self._storage.at(idx.row())
            if role is Qt.ItemDataRole.UserRole: return library
            if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
                return repr(library)
        return None

    def flags(self, idx: QModelIndex = QModelIndex()) -> Qt.ItemFlag:
        if self._is_valid_idx(idx):
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable  # type: ignore
        return Qt.ItemFlag.NoItemFlags

    def reset_rows(self):
        self.beginResetModel()
        self._storage.pop_all()
        self.endResetModel()

    def add_row(self, value: ZoteroLibrary):
        next_row = self.rowCount()
        self.beginInsertRows(QModelIndex(), next_row, next_row)
        self._storage.push(value)
        self.endInsertRows()

    def remove_row(self, row: int):
        if self._storage.in_bounds(row):
            self.beginRemoveRows(QModelIndex(), row, row)
            self._storage.pop(row)
            self.endRemoveRows()
        return None

    def update_row(self, row: int, value: ZoteroLibrary):
        if self._storage.in_bounds(row):
            self._storage.mutate(row, value)
            idx = self.index(row)
            self.dataChanged.emit(idx, idx, [
                Qt.ItemDataRole.UserRole,
                Qt.ItemDataRole.DisplayRole,
                Qt.ItemDataRole.ToolTipRole
            ])
