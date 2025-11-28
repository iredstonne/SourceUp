from typing import Any, Dict
from sourceup.collection.ZoteroCollection import ZoteroCollection
from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.item.ZoteroItemDataFactory import ZoteroItemDataFactory
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.casts import map_to_str, map_to_dict

class ZoteroDataMapper:
    @staticmethod
    def to_collection(_raw: Dict[str, Any]) -> ZoteroCollection:
        _collection_key = map_to_str(_raw.get("key"))
        _collection_data = map_to_dict(_raw.get("data"))
        _collection_name = map_to_str(_collection_data.get("name"))
        return ZoteroCollection(
            collection_key=_collection_key,
            collection_name=_collection_name
        )

    @staticmethod
    def to_item(_raw: Dict[str, Any]) -> ZoteroItem | None:
        _item_key = map_to_str(_raw.get("key"))
        _item_data = ZoteroItemDataFactory.from_data(map_to_dict(_raw.get("data")))
        _item_type = ZoteroItemType(_item_data.item_type())
        return ZoteroItem(
            item_key=_item_key,
            item_data=_item_data,
            item_type=_item_type
        )
