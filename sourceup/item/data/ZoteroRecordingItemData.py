from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroRecordingItemData(ZoteroBaseItemData):
    series_title: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    place: Optional[str] = None
    label: Optional[str] = None
    running_time: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        raise NotImplementedError

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroRecordingItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            series_title=map_to_str(_data.get("seriesTitle")),
            volume=map_to_str(_data.get("volume")),
            number_of_volumes=map_to_str(_data.get("numberOfVolumes")),
            place=map_to_str(_data.get("place")),
            label=map_to_str(_data.get("label")),
            running_time=map_to_str(_data.get("runningTime")),
            isbn=map_to_str(_data.get("isbn"))
        )
