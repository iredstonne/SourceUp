from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.casts import map_to_str
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType

@dataclass(frozen=True, slots=True)
class ZoteroVideoRecordingItemData(ZoteroBaseItemData):
    series_title: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    place: Optional[str] = None
    running_time: Optional[str] = None
    isbn: Optional[str] = None
    studio: Optional[str] = None
    video_recording_format: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.VIDEO_RECORDING

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Film"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroVideoRecordingItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            series_title=map_to_str(_data.get("seriesTitle")),
            volume=map_to_str(_data.get("volume")),
            number_of_volumes=map_to_str(_data.get("numberOfVolumes")),
            place=map_to_str(_data.get("place")),
            running_time=map_to_str(_data.get("runningTime")),
            isbn=map_to_str(_data.get("ISBN")),
            studio=map_to_str(_data.get("studio")),
            video_recording_format=map_to_str(_data.get("videoRecordingFormat"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Film
        # ProductionCompany: Mapped (studio)
        # CountryRegion: Mapped (place)
        # Distributor: Mapped (studio)
        # Medium: Mapped (video_recording_format)
        # StandardNumber: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.studio)
        add_bibliography_namespaced_element_if_missing(_source_element, "CountryRegion", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.studio)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.video_recording_format)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.isbn)
