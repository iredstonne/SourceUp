from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing, \
    add_bibliography_namespaced_role_element
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroAudioRecordingItemData(ZoteroBaseItemData):
    series_title: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    place: Optional[str] = None
    running_time: Optional[str] = None
    isbn: Optional[str] = None
    label: Optional[str] = None
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
            label=map_to_str(_data.get("label")),
            audio_recording_format=map_to_str(_data.get("audioRecordingFormat"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.PERFORMER,
            ZoteroCreatorType.CONTRIBUTOR
        ), "Performer", True)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.COMPOSER,
        ), "Composer", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.WORDS_BY,
        ), "Writer", False)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> SoundRecording
        # AlbumTitle: Mapped (series_title)
        # ProductionCompany: Mapped (label)
        # Medium: Mapped (audio_recording_format)
        # City: Mapped (place)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # RecordingNumber: Mapped (call_number)
        # StandardNumber: Mapped (isbn)
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "AlbumTitle", self.series_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.label)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.audio_recording_format)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "RecordingNumber", self.call_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.isbn)
