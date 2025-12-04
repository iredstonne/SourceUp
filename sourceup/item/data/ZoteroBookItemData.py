from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.exporter.wordbibxml_functions import add_common_book_bibliography_namespaced_element
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
            isbn=map_to_str(_data.get("isbn"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        super().map_to_bibxml(_source_element)

        add_common_book_bibliography_namespaced_element(
            _source_element,
            _volume=self.volume,
            _number_volumes=self.number_of_volumes,
            _edition=self.edition,
            _city=self.place,
            _publisher=self.publisher,
            _pages=self.num_pages,
            _standard_number=self.isbn
        )
