from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroCaseItemData(ZoteroBaseItemData):
    case_name: Optional[str] = None
    court: Optional[str] = None
    date_decided: Optional[str] = None
    docket_number: Optional[str] = None
    reporter: Optional[str] = None
    reporter_volume: Optional[str] = None
    first_page: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.CASE

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroCaseItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            case_name=map_to_str(_data.get("caseName")),
            court=map_to_str(_data.get("court")),
            date_decided=map_to_str(_data.get("dateDecided")),
            docket_number=map_to_str(_data.get("docketNumber")),
            reporter=map_to_str(_data.get("reporter")),
            reporter_volume=map_to_str(_data.get("reporterVolume")),
            first_page=map_to_str(_data.get("firstPage")),
            history=map_to_str(_data.get("history"))
        )
