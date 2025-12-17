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
class ZoteroReportItemData(ZoteroBaseItemData):
    report_number: Optional[str] = None
    report_type: Optional[str] = None
    series_title: Optional[str] = None
    institution: Optional[str] = None
    place: Optional[str] = None
    pages: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.REPORT

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "Report"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroReportItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            report_number=map_to_str(_data.get("reportNumber")),
            report_type=map_to_str(_data.get("reportType")),
            series_title=map_to_str(_data.get("seriesTitle")),
            place=map_to_str(_data.get("place")),
            institution=map_to_str(_data.get("institution")),
            pages=map_to_str(_data.get("pages"))
        )

    @override
    def map_creators_to_bibxml(self, _author_composite_element: Element):
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.AUTHOR,
            ZoteroCreatorType.CONTRIBUTOR
        ), "Author", True)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.SERIES_EDITOR,
        ), "Editor", False)
        add_bibliography_namespaced_role_element(_author_composite_element, self.creators, (
            ZoteroCreatorType.TRANSLATOR,
        ), "Translator", False)

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> Report
        # Department: Not mapped
        # Institution: Mapped (institution)
        # Publisher: Mapped (institution)
        # City: Mapped (place)
        # Pages: Mapped (pages)
        # ThesisType: Mapped (report_type)
        # StandardNumber: Mapped (report_number)
        # Medium: Not mapped
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "Institution", self.institution)
        add_bibliography_namespaced_element_if_missing(_source_element, "Publisher", self.institution)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "ThesisType", self.report_type)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.report_number)