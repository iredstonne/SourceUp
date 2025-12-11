from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBookItemData(ZoteroBaseItemData):
    series: Optional[str] = None
    series_number: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    edition: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    num_pages: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.BOOK

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Book"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBookItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            series=map_to_str(_data.get("series")),
            series_number=map_to_str(_data.get("seriesNumber")),
            volume=map_to_str(_data.get("volume")),
            number_of_volumes=map_to_str(_data.get("numberOfVolumes")),
            edition=map_to_str(_data.get("edition")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            num_pages=map_to_str(_data.get("numPages")),
            isbn=map_to_str(_data.get("ISBN"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Book
        # City: Mapped (city)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Mapped (publisher)
        # Volume: Mapped (volume)
        # NumberVolumes: Mapped (number_of_volumes)
        # StandardNumber: Mapped (isbn)
        # Pages: Mapped (num_pages)
        # Edition: Mapped (edition)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.publisher)
        add_bibliography_namespaced_element_if_missing(_source_element, "Volume", self.volume)
        add_bibliography_namespaced_element_if_missing(_source_element, "NumberVolumes", self.number_of_volumes)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.isbn)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.num_pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "Edition", self.edition)

