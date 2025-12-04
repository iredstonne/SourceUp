from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.exporter.wordbibxml_functions import add_common_book_bibliography_namespaced_element, \
    add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBookSectionItemData(ZoteroBaseItemData):
    book_title: Optional[str] = None
    series: Optional[str] = None
    series_number: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    edition: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    pages: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.BOOK_SECTION

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "BookSection"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBookSectionItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            book_title=map_to_str(_data.get("bookTitle")),
            series=map_to_str(_data.get("series")),
            series_number=map_to_str(_data.get("seriesNumber")),
            volume=map_to_str(_data.get("volume")),
            number_of_volumes=map_to_str(_data.get("numberOfVolumes")),
            edition=map_to_str(_data.get("edition")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            pages=map_to_str(_data.get("pages")),
            isbn=map_to_str(_data.get("isbn"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(
            _source_element,
            "BookTitle",
            self.book_title
        )

        add_common_book_bibliography_namespaced_element(
            _source_element,
            _volume=self.volume,
            _number_volumes=self.number_of_volumes,
            _edition=self.edition,
            _city=self.place,
            _publisher=self.publisher,
            _pages=self.pages,
            _standard_number=self.isbn
        )
