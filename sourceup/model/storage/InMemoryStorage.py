from typing import TypeVar, List, Iterable, Optional

from sourceup.model.storage.StorageProtocol import StorageProtocol

T = TypeVar("T")

class InMemoryStorage(StorageProtocol[T]):
    _items: List[T] = []

    def __init__(self, initial_items: Optional[Iterable[T]] = None):
        self._items = list(initial_items or [])

    def count(self) -> int:
        return len(self._items)

    def all(self) -> Iterable[T]:
        return list(self._items)

    def reset(self) -> None:
        self.fill([])

    def fill(self, items: Iterable[T]) -> None:
        self._items = list(items)

    def append(self, item: T) -> None:
        self._items.append(item)

    def remove_at(self, row: int) -> None:
        if self.in_bounds(row):
            self._items.pop(row)

    def replace_at(self, row: int, item: T) -> None:
        if self.in_bounds(row):
            self._items[row] = item

    def at(self, row: int) -> Optional[T]:
        return self._items[row] if self.in_bounds(row) else None

    def in_bounds(self, row: int) -> bool:
        return 0 <= row < self.count()

    def flush(self) -> None:
        raise NotImplementedError("flush() is not supported for InMemoryStorage")
