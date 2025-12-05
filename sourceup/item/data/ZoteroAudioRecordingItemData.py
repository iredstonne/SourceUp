from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
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
    def bibliography_source_type(cls):
        return "SoundRecording"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroAudioRecordingItemData":
        _recording_item_data = ZoteroRecordingItemData.map_from_data(_data)
        return cls(
            **{_recording_item_data_field.name: getattr(_recording_item_data, _recording_item_data_field.name)
               for _recording_item_data_field in fields(ZoteroRecordingItemData)},
            audio_recording_format=map_to_str(_data.get("audioRecordingFormat"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroRecordingItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.audio_recording_format)
