from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroStatuteItemData(ZoteroBaseItemData):
    code: Optional[str] = None
    code_number: Optional[str] = None
    public_law_number: Optional[str] = None
    date_enacted: Optional[str] = None
    pages: Optional[str] = None
    section: Optional[str] = None
    session: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.STATUTE

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroStatuteItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            code=map_to_str(_data.get("code")),
            code_number=map_to_str(_data.get("code_number")),
            public_law_number=map_to_str(_data.get("public_law_number")),
            date_enacted=map_to_str(_data.get("date_enacted")),
            pages=map_to_str(_data.get("pages")),
            section=map_to_str(_data.get("section")),
            session=map_to_str(_data.get("session")),
            history=map_to_str(_data.get("history"))
        )
