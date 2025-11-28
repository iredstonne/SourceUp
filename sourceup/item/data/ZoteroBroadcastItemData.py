from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBroadcastItemData(ZoteroBaseItemData):
    program_title: Optional[str] = None
    episode_number: Optional[str] = None
    place: Optional[str] = None
    network: Optional[str] = None
    running_time: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        raise NotImplementedError

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBroadcastItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            program_title=map_to_str(_data.get("programTitle")),
            episode_number=map_to_str(_data.get("episodeNumber")),
            place=map_to_str(_data.get("place")),
            network=map_to_str(_data.get("network")),
            running_time=map_to_str(_data.get("runningTime"))
        )
