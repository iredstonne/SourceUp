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
class ZoteroStatuteItemData(ZoteroBaseItemData):
    code: Optional[str] = None
    code_number: Optional[str] = None
    public_law_number: Optional[str] = None
    date_enacted: Optional[str] = None
    pages: Optional[str] = None
    section: Optional[str] = None
    session: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.STATUTE

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Report"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroStatuteItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            code=map_to_str(_data.get("code")),
            code_number=map_to_str(_data.get("codeNumber")),
            public_law_number=map_to_str(_data.get("publicLawNumber")),
            date_enacted=map_to_str(_data.get("dateEnacted")),
            pages=map_to_str(_data.get("pages")),
            section=map_to_str(_data.get("section")),
            session=map_to_str(_data.get("session")),
            history=map_to_str(_data.get("history"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR
        ), "Author", True)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Report
        # Department: Not mapped
        # Institution: Not mapped
        # Publisher: Not mapped
        # City: Not mapped
        # Pages: Mapped (pages)
        # ThesisType: Not mapped
        # StandardNumber: Mapped (public_law_number)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.public_law_number)
