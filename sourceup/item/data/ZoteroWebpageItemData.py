from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element
from sourceup.casts import map_to_str
from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemType import ZoteroItemType

@dataclass(frozen=True, slots=True)
class ZoteroWebpageItemData(ZoteroBaseItemData):
    website_title: Optional[str] = None
    website_type: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.WEBPAGE

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "InternetSite"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroWebpageItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            website_title=map_to_str(_data.get("websiteTitle")),
            website_type=map_to_str(_data.get("websiteType"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        # SourceType -> InternetSite
        # InternetSiteTitle: Mapped (website_title)
        # ProductionCompany: Not mapped
        # Version: Not mapped
        # StandardNumber: Not mapped
        # Medium: Mapped (website_type)
        # DOI: Not mapped

        add_bibliography_namespaced_element_if_missing(_source_element, "InternetSiteTitle", self.website_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "Medium", self.website_type)
