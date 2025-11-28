from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroPreprintItemData(ZoteroBaseItemData):
    genre: Optional[str] = None
    repository: Optional[str] = None
    archive_id: Optional[str] = None
    place: Optional[str] = None
    series: Optional[str] = None
    series_number: Optional[str] = None
    doi: Optional[str] = None
    citation_key: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.PREPRINT

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroPreprintItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            genre=map_to_str(_data.get("genre")),
            repository=map_to_str(_data.get("repository")),
            archive_id=map_to_str(_data.get("archiveID")),
            place=map_to_str(_data.get("place")),
            series=map_to_str(_data.get("series")),
            series_number=map_to_str(_data.get("seriesNumber")),
            doi=map_to_str(_data.get("doi")),
            citation_key=map_to_str(_data.get("citationKey")),
        )
