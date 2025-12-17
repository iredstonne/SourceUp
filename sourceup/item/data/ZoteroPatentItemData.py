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
class ZoteroPatentItemData(ZoteroBaseItemData):
    place: Optional[str] = None
    country: Optional[str] = None
    assignee: Optional[str] = None
    issuing_authority: Optional[str] = None
    patent_number: Optional[str] = None
    filling_date: Optional[str] = None
    pages: Optional[str] = None
    application_number: Optional[str] = None
    priority_numbers: Optional[str] = None
    issue_date: Optional[str] = None
    references: Optional[str] = None
    legal_status: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.PATENT

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Patent"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroPatentItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            place=map_to_str(_data.get("place")),
            country=map_to_str(_data.get("country")),
            assignee=map_to_str(_data.get("assignee")),
            issuing_authority=map_to_str(_data.get("issuingAuthority")),
            patent_number=map_to_str(_data.get("patentNumber")),
            filling_date=map_to_str(_data.get("fillingDate")),
            pages=map_to_str(_data.get("pages")),
            application_number=map_to_str(_data.get("applicationNumber")),
            priority_numbers=map_to_str(_data.get("priorityNumbers")),
            issue_date=map_to_str(_data.get("issueDate")),
            references=map_to_str(_data.get("references")),
            legal_status=map_to_str(_data.get("legalStatus"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.INVENTOR,
            ZoteroCreatorType.CONTRIBUTOR
        ),"Inventor", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.ATTORNEY_AGENT,
        ), "Editor", False)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Patent
        # CountryRegion: Mapped (country)
        # Type: Not mapped
        # PatentNumber: Mapped (patent_number)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "CountryRegion", self.country)
        add_bibliography_namespaced_element_if_missing(_source_element, "PatentNumber", self.patent_number)
