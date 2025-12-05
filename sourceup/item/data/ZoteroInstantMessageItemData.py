from dataclasses import dataclass, fields
from typing import override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData

@dataclass(frozen=True, slots=True)
class ZoteroInstantMessageItemData(ZoteroBaseItemData):

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.INSTANT_MESSAGE

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ElectronicSource"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroInstantMessageItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)}
        )
