from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroLetterItemData(ZoteroBaseItemData):
    letter_type: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.LETTER

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroLetterItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            letter_type=map_to_str(_data.get("letterType")),
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Misc
        # PublicationTitle: Mapped (title)
        # MediaType: Mapped "Letter"
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Not mapped
        # Pages: Not mapped
        # Volume: Not mapped
        # Edition: Not mapped
        # Number: Not mapped
        # StandardNumber: Not mapped
        # Medium: Mapped (letter_type)
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.title)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.letter_type)
