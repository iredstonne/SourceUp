from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroJournalArticleItemData(ZoteroBaseItemData):
    publication_title: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    series: Optional[str] = None
    series_title: Optional[str] = None
    series_text: Optional[str] = None
    journal_abreviation: Optional[str] = None
    doi: Optional[str] = None
    issn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.JOURNAL_ARTICLE

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroJournalArticleItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            publication_title=map_to_str(_data.get("publicationTitle")),
            volume=map_to_str(_data.get("volume")),
            issue=map_to_str(_data.get("issue")),
            pages=map_to_str(_data.get("pages")),
            series=map_to_str(_data.get("series")),
            series_title=map_to_str(_data.get("series_title")),
            series_text=map_to_str(_data.get("series_text")),
            journal_abreviation=map_to_str(_data.get("journal_abreviation")),
            doi=map_to_str(_data.get("doi")),
            issn=map_to_str(_data.get("issn"))
        )
