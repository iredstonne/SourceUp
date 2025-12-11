from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroDocumentItemData(ZoteroBaseItemData):
    publisher: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.DOCUMENT

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ElectronicSource"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroDocumentItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            publisher=map_to_str(_data.get("publisher"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> ElectronicSource
        # PublicationTitle: Mapped (title)
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # ProductionCompany: Mapped (publisher)
        # Publisher: Mapped (publisher)
        # Edition: Not mapped
        # Medium: Not mapped
        # Volume: Not mapped
        # StandardNumber: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.title)
        add_bibliography_namespaced_element_if_missing(_source_element, "ProductionCompany", self.publisher)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.publisher)
