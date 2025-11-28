from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroMapItemData(ZoteroBaseItemData):
    map_type: Optional[str] = None
    scale: Optional[str] = None
    series_title: Optional[str] = None
    edition: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.MAP

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroMapItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            map_type=map_to_str(_data.get("mapType")),
            scale=map_to_str(_data.get("scale")),
            series_title=map_to_str(_data.get("seriesTitle")),
            edition=map_to_str(_data.get("edition")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            isbn=map_to_str(_data.get("isbn")),
        )
