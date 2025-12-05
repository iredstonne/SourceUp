from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroArtworkItemData(ZoteroBaseItemData):
    artwork_medium: Optional[str] = None
    artwork_size: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.ARTWORK

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Art"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroArtworkItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            artwork_medium=map_to_str(_data.get("artworkMedium")),
            artwork_size=map_to_str(_data.get("artworkSize"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.artwork_medium)
