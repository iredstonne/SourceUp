from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroConferencePaperItemData(ZoteroBaseItemData):
    proceedings_title: Optional[str] = None
    conference_name: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    volume: Optional[str] = None
    pages: Optional[str] = None
    series: Optional[str] = None
    doi: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.CONFERENCE_PAPER

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ConferenceProceedings"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroConferencePaperItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            proceedings_title=map_to_str(_data.get("proceedingsTitle")),
            conference_name=map_to_str(_data.get("conferenceName")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            volume=map_to_str(_data.get("volume")),
            pages=map_to_str(_data.get("pages")),
            series=map_to_str(_data.get("series")),
            doi=map_to_str(_data.get("DOI")),
            isbn=map_to_str(_data.get("ISBN"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(_source_element, "BookTitle", self.proceedings_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "ConferenceName", self.conference_name)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.publisher)
        add_bibliography_namespaced_element_if_missing(_source_element, "Volume", self.volume)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "DOI", self.doi)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.isbn)
