from typing import Generic, TypeVar, Optional, Iterable, Union, override
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.ui.model.data_provider.DataProviderProtocol import DataProviderProtocol
from sourceup.ui.model.storage.InMemoryStorage import InMemoryStorage
from sourceup.ui.model.storage.StorageProtocol import StorageProtocol

T = TypeVar("T")

class GenericListModel(QAbstractListModel, Generic[T]):
    _storage: Optional[StorageProtocol[T]]
    _data_provider: Optional[DataProviderProtocol[T]]

    def __init__(
        self,
        _initial_row_items: Optional[Iterable[T]] = None,
        _storage_impl: Optional[StorageProtocol[T]] = None,
        _data_provider_impl: DataProviderProtocol[T] = None
    ):
        super().__init__()
        self._storage = _storage_impl or InMemoryStorage(_initial_row_items)
        if not _data_provider_impl: raise ValueError("GenericListModel requires DataProvider implementation")
        self._data_provider = _data_provider_impl

    @property
    def row_items(self) -> Iterable[ZoteroItem]:
        return self._storage.all()

    @override
    def rowCount(self, _: QModelIndex = QModelIndex()) -> int:
        return self._storage.count()

    @override
    def data(self, _model_idx: QModelIndex, _role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Optional[T]:
        _row = _model_idx.row()
        if not _model_idx.isValid() or not self._storage.in_bounds(_row):
            return None
        _value = self._storage.at(_row)
        if _value is None:
            return None
        return self._data_provider.data(_value, _role)

    @override
    def flags(self, _model_idx: QModelIndex, _role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Union[Qt.ItemFlag]:
        _row = _model_idx.row()
        if not _model_idx.isValid() or not self._storage.in_bounds(_row):
            return Qt.ItemFlag.NoItemFlags
        _value = self._storage.at(_row)
        if _value is None:
            return Qt.ItemFlag.NoItemFlags
        return self._data_provider.flags(_value)

    def clear_rows(self):
        self.beginResetModel()
        self._storage.fill([])
        self.endResetModel()

    def set_rows(self, _row_items: Iterable[T]):
        self.beginResetModel()
        self._storage.fill(_row_items)
        self.endResetModel()

    def append_row_item(self, _row_item: T):
        _row = self._storage.count()
        self.beginInsertRows(QModelIndex(), _row, _row)
        self._storage.append(_row_item)
        self.endInsertRows()

    def remove_row_item_at(self, _row: int):
        if not self._storage.in_bounds(_row):
            return
        self.beginRemoveRows(QModelIndex(), _row, _row)
        self._storage.remove_at(_row)
        self.endRemoveRows()

    def replace_row_item_at(self, _row: int, _value: T):
        if not self._storage.in_bounds(_row):
            return
        self._storage.replace_at(_row, _value)
        _index = self.index(_row)
        self.dataChanged.emit(_index, _index, self.roleNames())

    def row_item_at(self, _row: int) -> Optional[T]:
        return self._storage.at(_row)
