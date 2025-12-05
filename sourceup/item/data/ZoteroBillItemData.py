from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBillItemData(ZoteroBaseItemData):
    bill_number: Optional[str] = None
    code: Optional[str] = None
    code_volume: Optional[str] = None
    section: Optional[str] = None
    code_pages: Optional[str] = None
    legislative_body: Optional[str] = None
    session: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.BILL

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBillItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            bill_number=map_to_str(_data.get("billNumber")),
            code=map_to_str(_data.get("code")),
            code_volume=map_to_str(_data.get("codeVolume")),
            section=map_to_str(_data.get("section")),
            code_pages=map_to_str(_data.get("codePages")),
            legislative_body=map_to_str(_data.get("legislativeBody")),
            session=map_to_str(_data.get("session")),
            history=map_to_str(_data.get("history"))
        )
