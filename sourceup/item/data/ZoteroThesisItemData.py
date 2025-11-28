from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroThesisItemData(ZoteroBaseItemData):
    thesis_type: Optional[str] = None
    university: Optional[str] = None
    place: Optional[str] = None
    num_pages: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.THESIS

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroThesisItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            thesis_type=map_to_str(_data.get("manuscriptType")),
            university=map_to_str(_data.get("university")),
            place=map_to_str(_data.get("place")),
            num_pages=map_to_str(_data.get("numPages"))
        )
