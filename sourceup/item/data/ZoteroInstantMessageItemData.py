from dataclasses import dataclass, fields
from typing import override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing, \
    add_bibliography_namespaced_role_element
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData

@dataclass(frozen=True, slots=True)
class ZoteroInstantMessageItemData(ZoteroBaseItemData):

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.INSTANT_MESSAGE

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ElectronicSource"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroInstantMessageItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)}
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR,
            ZoteroCreatorType.RECIPIENT,
        ), "Author", True)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> ElectronicSource
        # PublicationTitle: Mapped (title)
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # ProductionCompany: Not mapped
        # Publisher: Not mapped
        # Edition: Not mapped
        # Medium: Not mapped
        # Volume: Not mapped
        # StandardNumber: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element,"PublicationTitle", self.title)
