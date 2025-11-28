from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.data.ZoteroRecordingItemData import ZoteroRecordingItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroAudioRecordingItemData(ZoteroRecordingItemData):
    audio_recording_format: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.AUDIO_RECORDING

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroAudioRecordingItemData":
        _recording_item_data = ZoteroRecordingItemData.map_from_data(_data)
        return cls(
            **{_recording_item_data_field.name: getattr(_recording_item_data, _recording_item_data_field.name)
               for _recording_item_data_field in fields(ZoteroRecordingItemData)},
            audio_recording_format=map_to_str(_data.get("audioRecordingFormat"))
        )
