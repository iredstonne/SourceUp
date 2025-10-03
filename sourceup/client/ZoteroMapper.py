from typing import Any, Dict
from sourceup.data.collection.ZoteroCollection import ZoteroCollection
from sourceup.data.item.ZoteroItem import ZoteroItem
from sourceup.data.item.ZoteroBaseItemData import ZoteroItemData
from sourceup.data.item.ZoteroItemDataFactory import ZoteroItemDataFactory
from sourceup.data.item.ZoteroItemType import ZoteroItemType
from sourceup.casts import map_to_str, map_to_dict

class ZoteroMapper:
    @staticmethod
    def to_collection(raw: Dict[str, Any]) -> ZoteroCollection:
        _key = map_to_str(raw.get("key"))
        _data = map_to_dict(raw.get("data"))
        _name = map_to_str(_data.get("name"))
        return ZoteroCollection(
            key=map_to_str(raw.get("key")),
            name=_name
        )

    @staticmethod
    def to_item(raw: Dict[str, Any]) -> ZoteroItem | None:
        _data = map_to_dict(raw.get("data"))
        _item_data = ZoteroItemDataFactory.from_data(_data)
        _item_type = ZoteroItemType(_item_data.item_type())
        return ZoteroItem(
            key=map_to_str(raw.get("key")),
            item_data=_item_data,
            item_type=_item_type
        )
