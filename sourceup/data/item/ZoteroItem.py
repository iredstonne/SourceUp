from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING: from sourceup.data.item.ZoteroItemType import ZoteroItemType
if TYPE_CHECKING: from sourceup.data.item.ZoteroBaseItemData import ZoteroBaseItemData

@dataclass(frozen=True, slots=True)
class ZoteroItem:
    key: str
    item_data: "ZoteroBaseItemData"
    item_type: "ZoteroItemType"

    def __repr__(self):
        return f"ZoteroItem({self.key}, {self.item_data.title})"

    def __str__(self):
        return self.__repr__()
