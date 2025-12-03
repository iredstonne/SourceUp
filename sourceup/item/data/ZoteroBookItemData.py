from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.exporter.wordbibxml_functions import create_bibliography_namespaced_element
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
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

        # NOTE: Series is not available in BibXML

        # NOTE: Series Number is not available in BibXML

        if self.volume:
            _volume_element = create_bibliography_namespaced_element("Volume")
            _volume_element.text = str(self.volume)
            _source_element.append(_volume_element)

        if self.number_of_volumes:
            _number_volumes_element = create_bibliography_namespaced_element("NumberVolumes")
            _number_volumes_element.text = str(self.number_of_volumes)
            _source_element.append(_number_volumes_element)

        if self.edition:
            _edition_element = create_bibliography_namespaced_element("Edition")
            _edition_element.text = str(self.edition)
            _source_element.append(_edition_element)

        if self.place:
            _city_element = create_bibliography_namespaced_element("City")
            _city_element.text = str(self.place)
            _source_element.append(_city_element)

        if self.publisher:
            _publisher_element = create_bibliography_namespaced_element("Publisher")
            _publisher_element.text = str(self.publisher)
            _source_element.append(_publisher_element)

        if self.num_pages:
            _pages_element = create_bibliography_namespaced_element("Pages")
            _pages_element.text = str(self.num_pages)
            _source_element.append(_pages_element)

        if self.isbn:
            _isbn_element = create_bibliography_namespaced_element("StandardNumber")
            _isbn_element.text = str(self.isbn)
            _source_element.append(_isbn_element)
