from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.casts import map_to_str
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType


@dataclass(frozen=True, slots=True)
class ZoteroTvBroadcastItemData(ZoteroBaseItemData):
    program_title: Optional[str] = None
    episode_number: Optional[str] = None
    place: Optional[str] = None
    network: Optional[str] = None
    running_time: Optional[str] = None
    video_recording_format: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.TV_BROADCAST

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Film"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBaseItemData":
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

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Film
        # ProductionCompany: Mapped (network)
        # CountryRegion: Not mapped
        # Distributor: Mapped (network)
        # Medium: Mapped (audio_recording_format)
        # RecordingNumber: Mapped (episode_number)
        # StandardNumber: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.network)
        add_bibliography_namespaced_element_if_missing(_source_element, "Distributor", self.network)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.video_recording_format)
        add_bibliography_namespaced_element_if_missing(_source_element, "RecordingNumber", self.episode_number)
