from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.data.ZoteroBookItemData import ZoteroBookItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBookSectionItemData(ZoteroBookItemData):
    book_title: Optional[str] = None
    pages: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.BOOK_SECTION

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBookSectionItemData":
        _book_item_data = ZoteroBookItemData.map_from_data(_data)
        return cls(
            **{_book_item_data_field.name: getattr(_book_item_data, _book_item_data_field.name)
               for _book_item_data_field in fields(ZoteroBookItemData)},
            book_title=map_to_str(_data.get("bookTitle")),
            pages=map_to_str(_data.get("pages"))
        )
