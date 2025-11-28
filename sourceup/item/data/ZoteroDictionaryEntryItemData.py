from dataclasses import dataclass, fields
from typing import override, Dict, Any, Optional
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroDictionaryEntryItemData(ZoteroBaseItemData):
    dictionary_title: Optional[str] = None
    series: Optional[str] = None
    series_number: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    edition: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    pages: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.DICTIONARY_ENTRY

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroDictionaryEntryItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            dictionary_title=map_to_str(_data.get("dictionaryTitle")),
            series=map_to_str(_data.get("series")),
            series_number=map_to_str(_data.get("seriesNumber")),
            volume=map_to_str(_data.get("volume")),
            number_of_volumes=map_to_str(_data.get("numberOfVolumes")),
            edition=map_to_str(_data.get("edition")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            pages=map_to_str(_data.get("pages")),
            isbn=map_to_str(_data.get("isbn"))
        )
