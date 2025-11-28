from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroNoteItemData(ZoteroBaseItemData):

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.NOTE

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroNoteItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)}
        )
