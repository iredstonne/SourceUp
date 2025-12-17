from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.creator.ZoteroCreatorType import ZoteroCreatorType
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing, \
    add_bibliography_namespaced_role_element
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroManuscriptItemData(ZoteroBaseItemData):
    manuscript_type: Optional[str] = None
    place: Optional[str] = None
    num_pages: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.MANUSCRIPT

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Report"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroManuscriptItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            manuscript_type=map_to_str(_data.get("manuscriptType")),
            place=map_to_str(_data.get("place")),
            num_pages=map_to_str(_data.get("numPages"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR
        ), "Author", True)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.TRANSLATOR,
        ), "Translator", False)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Report
        # Department: Not mapped
        # Institution: Not mapped
        # Publisher: Not mapped
        # City: Mapped (place)
        # Pages: Mapped (num_pages)
        # ThesisType: Mapped (manuscript_type)
        # StandardNumber: Not mapped
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.num_pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "ThesisType", self.manuscript_type)
