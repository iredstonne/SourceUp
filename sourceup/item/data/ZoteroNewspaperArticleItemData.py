from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroNewspaperArticleItemData(ZoteroBaseItemData):
    publication_title: Optional[str] = None
    place: Optional[str] = None
    edition: Optional[str] = None
    section: Optional[str] = None
    pages: Optional[str] = None
    issn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.NEWSPAPER_ARTICLE

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroNewspaperArticleItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            publication_title=map_to_str(_data.get("publication_title")),
            place=map_to_str(_data.get("place")),
            edition=map_to_str(_data.get("edition")),
            section=map_to_str(_data.get("section")),
            pages=map_to_str(_data.get("pages")),
            issn=map_to_str(_data.get("issn")),
        )
