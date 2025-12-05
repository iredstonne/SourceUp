from typing import TYPE_CHECKING, Dict, Any
if TYPE_CHECKING: from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemDataCache import ZoteroItemDataCache

class ZoteroItemDataFactory:
    _CACHE = ZoteroItemDataCache()

    @classmethod
    def from_data(cls, _data: Dict[str, Any]) -> "ZoteroBaseItemData":
        _item_type = _data.get("itemType")
        if not _item_type:
            raise ValueError(f"Missing 'itemType' in data from Zotero: {_data!r}")
        _memoized_item_data_cls = cls._CACHE.resolve_item_data_from_memo(_item_type)
        if _memoized_item_data_cls is None:
            raise ValueError(f"Unhandled Zotero item type '{_item_type}'")
        return _memoized_item_data_cls.map_from_data(_data)
