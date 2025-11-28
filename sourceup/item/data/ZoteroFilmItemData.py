from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroFilmItemData(ZoteroBaseItemData):
    distributor: Optional[str] = None
    genre: Optional[str] = None
    video_recording_format: Optional[str] = None
    running_time: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.FILM

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroFilmItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            distributor=map_to_str(_data.get("distributor")),
            genre=map_to_str(_data.get("genre")),
            video_recording_format=map_to_str(_data.get("videoRecordingFormat")),
            running_time=map_to_str(_data.get("runningTime"))
        )
