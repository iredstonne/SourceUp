from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroStandardItemData(ZoteroBaseItemData):
    organization: Optional[str] = None
    committee: Optional[str] = None
    type: Optional[str] = None
    number: Optional[str] = None
    version_number: Optional[str] = None
    status: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.STANDARD

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroStandardItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            organization=map_to_str(_data.get("organization")),
            committee=map_to_str(_data.get("committee")),
            type=map_to_str(_data.get("type")),
            number=map_to_str(_data.get("number")),
            version_number=map_to_str(_data.get("version_number")),
            status=map_to_str(_data.get("status"))
        )
