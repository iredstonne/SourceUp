from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
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
    def bibliography_source_type(cls):
        return "Film"

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

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.distributor)
        add_bibliography_namespaced_element_if_missing(_source_element, "Type", self.genre)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.video_recording_format)
        add_bibliography_namespaced_element_if_missing(_source_element, "Duration", self.running_time)
