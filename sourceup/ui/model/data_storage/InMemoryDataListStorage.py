from typing import TypeVar, Iterable, Optional
from sourceup.ui.model.data_storage.DataListStorageProtocol import DataListStorageProtocol

T = TypeVar("T")

class InMemoryDataListStorage(DataListStorageProtocol[T]):
    def __init__(self, initial_items: Optional[Iterable[T]] = None):
        self._items = list(initial_items or [])

    def count(self) -> int:
        return len(self._items)

    def all(self) -> Iterable[T]:
        return list(self._items)

    def fill(self, _items: Iterable[T]) -> None:
        self._items = list(_items)

    def append(self, _item: T) -> None:
        self._items.append(_item)

    def remove_at(self, _index: int) -> None:
        if self.in_bounds(_index):
            self._items.pop(_index)

    def replace_at(self, _index: int, _item: T) -> None:
        if self.in_bounds(_index):
            self._items[_index] = _item

    def at(self, _index: int) -> Optional[T]:
        return self._items[_index] if self.in_bounds(_index) else None

    def in_bounds(self, _index: int) -> bool:
        return 0 <= _index < self.count()
