from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing, \
    add_bibliography_namespaced_role_element
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroPodcastItemData(ZoteroBaseItemData):
    series_title: Optional[str] = None
    episode_number: Optional[str] = None
    audio_file_type: Optional[str] = None
    running_time: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.PODCAST

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Interview"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroPodcastItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            series_title=map_to_str(_data.get("seriesTitle")),
            episode_number=map_to_str(_data.get("episodeNumber")),
            audio_file_type=map_to_str(_data.get("audioFileType")),
            running_time=map_to_str(_data.get("runningTime"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.PODCASTER,
            ZoteroCreatorType.CONTRIBUTOR,
        ), "Interviewer", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.GUEST,
        ), "Interviewee", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.TRANSLATOR,
        ), "Translator", False)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Interview
        # AlbumTitle: Mapped (series_title)
        # Publisher: Not mapped
        # Distributor: Not mapped
        # Station: Not mapped
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Pages: Not mapped
        # StandardNumber: Not mapped
        # Medium: Mapped (audio_file_type)
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "AlbumTitle", self.series_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.audio_file_type)

