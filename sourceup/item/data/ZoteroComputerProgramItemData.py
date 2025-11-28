from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroComputerProgramItemData(ZoteroBaseItemData):
    series_title: Optional[str] = None
    version_number: Optional[str] = None
    system: Optional[str] = None
    place: Optional[str] = None
    company: Optional[str] = None
    programming_language: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.COMPUTER_PROGRAM

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroComputerProgramItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            series_title=map_to_str(_data.get("seriesTitle")),
            version_number=map_to_str(_data.get("version_number")),
            system=map_to_str(_data.get("system")),
            place=map_to_str(_data.get("place")),
            company=map_to_str(_data.get("company")),
            programming_language=map_to_str(_data.get("programming_language")),
            isbn=map_to_str(_data.get("isbn"))
        )
