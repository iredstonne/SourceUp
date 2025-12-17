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
class ZoteroCaseItemData(ZoteroBaseItemData):
    case_name: Optional[str] = None
    court: Optional[str] = None
    date_decided: Optional[str] = None
    docket_number: Optional[str] = None
    reporter: Optional[str] = None
    reporter_volume: Optional[str] = None
    first_page: Optional[str] = None
    history: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.CASE

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Misc"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroCaseItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{base_item_data_field.name: getattr(_base_item_data, base_item_data_field.name)
               for base_item_data_field in fields(ZoteroBaseItemData)},
            case_name=map_to_str(_data.get("caseName")),
            court=map_to_str(_data.get("court")),
            date_decided=map_to_str(_data.get("dateDecided")),
            docket_number=map_to_str(_data.get("docketNumber")),
            reporter=map_to_str(_data.get("reporter")),
            reporter_volume=map_to_str(_data.get("reporterVolume")),
            first_page=map_to_str(_data.get("firstPage")),
            history=map_to_str(_data.get("history"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR,
            ZoteroCreatorType.COUNSEL
        ), "Author", True)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Misc
        # PublicationTitle: Mapped (reporter)
        # MediaType: Mapped "Case"
        # City: Not mapped
        # StateProvince: Not mapped
        # CountryRegion: Not mapped
        # Publisher: Mapped (court)
        # Pages: Mapped (first_page)
        # Volume: Mapped (reporter_volume)
        # Edition: Not mapped
        # Number: Mapped (docket_number)
        # StandardNumber: Mapped (docket_number)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "PublicationTitle", self.reporter)
        add_bibliography_namespaced_element_if_missing(_source_element, "MediaType", "Case")
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.court)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.first_page)
        add_bibliography_namespaced_element_if_missing(_source_element, "Volume", self.reporter_volume)
        add_bibliography_namespaced_element_if_missing(_source_element, "Number", self.docket_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.docket_number)
