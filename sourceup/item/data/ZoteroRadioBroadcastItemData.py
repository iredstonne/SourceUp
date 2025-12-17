from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.casts import map_to_str
from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing, \
    add_bibliography_namespaced_role_element
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType

@dataclass(frozen=True, slots=True)
class ZoteroRadioBroadcastItemData(ZoteroBaseItemData):
    program_title: Optional[str] = None
    episode_number: Optional[str] = None
    place: Optional[str] = None
    network: Optional[str] = None
    running_time: Optional[str] = None
    audio_recording_format: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.RADIO_BROADCAST

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "SoundRecording"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroRadioBroadcastItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            program_title=map_to_str(_data.get("programTitle")),
            episode_number=map_to_str(_data.get("episodeNumber")),
            place=map_to_str(_data.get("place")),
            network=map_to_str(_data.get("network")),
            running_time=map_to_str(_data.get("runningTime")),
            audio_recording_format=map_to_str(_data.get("audioRecordingFormat"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.CAST_MEMBER,
            ZoteroCreatorType.GUEST,
            ZoteroCreatorType.CONTRIBUTOR
        ), "Performer", True)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.PRODUCER,
        ), "ProducerName", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.DIRECTOR,
        ), "Director", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.SCRIPT_WRITER,
        ), "Writer", False)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> SoundRecording
        # AlbumTitle: Mapped (program_title)
        # ProductionCompany: Mapped (network)
        # Medium: Mapped (audio_recording_format)
        # City: Mapped (place)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # RecordingNumber: Mapped (call_number)
        # StandardNumber: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "AlbumTitle", self.program_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.network)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.audio_recording_format)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "RecordingNumber", self.episode_number)

