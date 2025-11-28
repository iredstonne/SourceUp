from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroHearingItemData(ZoteroBaseItemData):
    committee: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    number_of_volumes: Optional[str] = None
    document_number: Optional[str] = None
    pages: Optional[str] = None
    legislative_body: Optional[str] = None
    session: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.HEARING

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroHearingItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            committee=map_to_str(_data.get("committee")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            number_of_volumes=map_to_str(_data.get("number_of_volumes")),
            document_number=map_to_str(_data.get("document_number")),
            pages=map_to_str(_data.get("pages")),
            legislative_body=map_to_str(_data.get("legislative_body")),
            session=map_to_str(_data.get("session")),
            history=map_to_str(_data.get("history"))
        )
