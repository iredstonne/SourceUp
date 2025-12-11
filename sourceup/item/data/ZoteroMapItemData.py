from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroMapItemData(ZoteroBaseItemData):
    map_type: Optional[str] = None
    scale: Optional[str] = None
    series_title: Optional[str] = None
    edition: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.MAP

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroMapItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            map_type=map_to_str(_data.get("mapType")),
            scale=map_to_str(_data.get("scale")),
            series_title=map_to_str(_data.get("seriesTitle")),
            edition=map_to_str(_data.get("edition")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            isbn=map_to_str(_data.get("isbn")),
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Misc
        # PublicationTitle: Mapped (series_title)
        # MediaType: Mapped "Map"
        # City: Mapped (place)
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Mapped (publisher)
        # Pages: Not mapped
        # Volume: Not mapped
        # Edition: Mapped (edition)
        # Number: Not mapped
        # StandardNumber: Mapped (isbn)
        # Medium: Mapped (map_type)
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.series_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.publisher)
        add_bibliography_namespaced_element_if_missing(_source_element, "Edition", self.edition)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.isbn)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.map_type)
