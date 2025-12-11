from dataclasses import dataclass, fields
from typing import override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType

@dataclass(frozen=True, slots=True)
class ZoteroAttachmentItemData(ZoteroBaseItemData):

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.ATTACHMENT

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Misc"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroAttachmentItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)}
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Misc
        # PublicationTitle: Mapped (title)
        # MediaType: Mapped "Attachment"
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Not mapped
        # Pages: Not mapped
        # Volume: Not mapped
        # Edition: Not mapped
        # Number: Not mapped
        # StandardNumber: Not mapped
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.title)
        add_bibliography_namespaced_element_if_missing(_source_element, "MediaType", "Attachment")
