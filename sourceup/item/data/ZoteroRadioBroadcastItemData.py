from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.data.ZoteroBroadcastItemData import ZoteroBroadcastItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroRadioBroadcastItemData(ZoteroBroadcastItemData):
    audio_recording_format: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.RADIO_BROADCAST

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroRadioBroadcastItemData":
        _broadcast_item_data = ZoteroBroadcastItemData.map_from_data(_data)
        return cls(
            **{_broadcast_item_data_field.name: getattr(_broadcast_item_data, _broadcast_item_data_field.name)
               for _broadcast_item_data_field in fields(ZoteroBroadcastItemData)},
            audio_recording_format=map_to_str(_data.get("audioRecordingFormat"))
        )
