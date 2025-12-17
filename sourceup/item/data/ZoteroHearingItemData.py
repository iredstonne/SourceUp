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
class ZoteroHearingItemData(ZoteroBaseItemData):
    committee: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    number_of_volumes: Optional[str] = None
    document_number: Optional[str] = None
    pages: Optional[str] = None
    legislative_body: Optional[str] = None
    session: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.HEARING

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Hearing"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroHearingItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            committee=map_to_str(_data.get("committee")),
            place=map_to_str(_data.get("place")),
            publisher=map_to_str(_data.get("publisher")),
            number_of_volumes=map_to_str(_data.get("numberOfVolumes")),
            document_number=map_to_str(_data.get("documentNumber")),
            pages=map_to_str(_data.get("pages")),
            legislative_body=map_to_str(_data.get("legislativeBody")),
            session=map_to_str(_data.get("session")),
            history=map_to_str(_data.get("history"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR,
        ), "Author", True)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Hearing
        # CaseNumber: Mapped (document_number)
        # Reporter: Mapped (committee)
        # City: Mapped (place)
        # Court: Mapped (legislative_body)
        # AbbreviatedCaseNumber: Mapped (document_number)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "CaseNumber", self.document_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "Reporter", self.committee)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Court", self.legislative_body)
        add_bibliography_namespaced_element_if_missing(_source_element, "AbbreviatedCaseNumber", self.document_number)


