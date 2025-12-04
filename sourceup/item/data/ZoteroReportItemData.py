from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import create_bibliography_namespaced_element, \
    add_bibliography_namespaced_element_if_missing
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
    num_pages: Optional[str] = None

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
            institution=map_to_str(_data.get("institution")),
            place=map_to_str(_data.get("place")),
            num_pages=map_to_str(_data.get("numPages"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(_source_element, "Number", self.report_number)
        add_bibliography_namespaced_element_if_missing(_source_element, "Institution", self.institution)
        add_bibliography_namespaced_element_if_missing(_source_element, "City", self.place)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.num_pages)
