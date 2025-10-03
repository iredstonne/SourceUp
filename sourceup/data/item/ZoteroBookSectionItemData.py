from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.casts import map_to_str
from sourceup.data.item.ZoteroBookItemData import ZoteroBookItemData

@dataclass(frozen=True, slots=True)
class ZoteroBookSectionItemData(ZoteroBookItemData):
    book_title: Optional[str] = None
    pages: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> str:
        return "bookSection"

    @override
    @classmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroBookSectionItemData":
        book_item_data = super().map_from_data(data)
        return cls(
            **{field.name: getattr(book_item_data, field.name) for field in fields(ZoteroBookItemData)},
            book_title=map_to_str(data.get("bookTitle")),
            pages=map_to_str(data.get("pages"))
        )
