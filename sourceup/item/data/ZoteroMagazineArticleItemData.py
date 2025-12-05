from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.exporter.wordbibxml_functions import add_bibliography_namespaced_element_if_missing
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroMagazineArticleItemData(ZoteroBaseItemData):
    publication_title: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    issn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.MAGAZINE_ARTICLE

    @override
    @classmethod
    def bibliography_source_type(cls):
        return "ArticleInAPeriodical"

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroMagazineArticleItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            publication_title=map_to_str(_data.get("publicationTitle")),
            volume=map_to_str(_data.get("volume")),
            issue=map_to_str(_data.get("issue")),
            pages=map_to_str(_data.get("pages")),
            issn=map_to_str(_data.get("ISSN")),
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)

        add_bibliography_namespaced_element_if_missing(_source_element, "PeriodicalTitle", self.publication_title)
        add_bibliography_namespaced_element_if_missing(_source_element, "Volume", self.volume)
        add_bibliography_namespaced_element_if_missing(_source_element, "Issue", self.issue)
        add_bibliography_namespaced_element_if_missing(_source_element, "Pages", self.pages)
        add_bibliography_namespaced_element_if_missing(_source_element, "StandardNumber", self.issn)
