from typing import Generic, TypeVar, Optional, Iterable, Union, override
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from sourceup.data.item.ZoteroItem import ZoteroItem
from sourceup.model.provider.ItemDataProviderProtocol import ItemDataProviderProtocol
from sourceup.model.storage.InMemoryStorage import InMemoryStorage
from sourceup.model.storage.StorageProtocol import StorageProtocol

T = TypeVar("T")

class GenericListModel(QAbstractListModel, Generic[T]):
    _storage: Optional[StorageProtocol[T]]
    _item_data_provider: Optional[ItemDataProviderProtocol[T]]

    def __init__(
        self,
        initial_row_items: Optional[Iterable[T]] = None,
        storage: Optional[StorageProtocol[T]] = None,
        item_data_provider: ItemDataProviderProtocol[T] = None
    ):
        super().__init__()
        self._storage = storage or InMemoryStorage(initial_row_items)
        if not item_data_provider:
            raise ValueError("GenericListModel requires ItemDataProvider implementation")
        self._item_data_provider = item_data_provider

    @property
    def row_items(self) -> Iterable[ZoteroItem]:
        return self._storage.all()

    @override
    def rowCount(self, _: QModelIndex = QModelIndex()) -> int:
        return self._storage.count()

    @override
    def data(self, idx: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Optional[T]:
        row = idx.row()
        if not idx.isValid() or not self._storage.in_bounds(row):
            return None
        value = self._storage.at(row)
        if value is None:
            return None
        return self._item_data_provider.data(value, role)

    @override
    def flags(self, idx: QModelIndex, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Union[Qt.ItemFlag]:
        row = idx.row()
        if not idx.isValid() or not self._storage.in_bounds(row):
            return Qt.ItemFlag.NoItemFlags
        value = self._storage.at(row)
        if value is None:
            return Qt.ItemFlag.NoItemFlags
        return self._item_data_provider.flags(value)

    def reset_rows(self) -> None:
        self.beginResetModel()
        self._storage.reset()
        self.endResetModel()

    def fill_rows(self, row_items: Iterable[T]) -> None:
        self.beginResetModel()
        self._storage.fill(row_items)
        self.endResetModel()

    def append_row(self, row: T) -> None:
        next_row = self.rowCount()
        self.beginInsertRows(QModelIndex(), next_row, next_row)
        self._storage.append(row)
        self.endInsertRows()

    def remove_row_at(self, row: int) -> None:
        if self._storage.in_bounds(row):
            self.beginRemoveRows(QModelIndex(), row, row)
            self._storage.remove_at(row)
            self.endRemoveRows()

    def replace_row_at(self, row: int, row_item: T) -> None:
        if self._storage.in_bounds(row):
            self._storage.replace_at(row, row_item)
            updated_idx = self.index(row)
            self.dataChanged.emit(updated_idx, updated_idx, set(self._item_data_provider.roles()))

    def row_at(self, row: int) -> Optional[T]:
        return self._storage.at(row) if self._storage.in_bounds(row) else None
