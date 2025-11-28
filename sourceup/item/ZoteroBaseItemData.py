from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any
from sourceup.creator.ZoteroCreator import ZoteroCreator
from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroBaseItemData:
    title: str
    creators: Tuple["ZoteroCreator", ...] = field(default_factory=tuple)
    abstract_note: Optional[str] = None
    date: Optional[str] = None
    language: Optional[str] = None
    short_title: Optional[str] = None
    url: Optional[str] = None
    access_date: Optional[str] = None
    archive: Optional[str] = None
    archive_location: Optional[str] = None
    library_catalog: Optional[str] = None
    call_number: Optional[str] = None
    rights: Optional[str] = None
    extra: Optional[str] = None

    @classmethod
    def item_type(cls) -> ZoteroItemType:
        raise NotImplementedError

    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroBaseItemData":
        return cls(
            title=map_to_str(_data.get("title")),
            creators=tuple(ZoteroCreator.map_from_data(_creator_data) for _creator_data in _data.get("creators") or ()),
            abstract_note=map_to_str(_data.get("abstractNote")),
            date=map_to_str(_data.get("date")),
            language=map_to_str(_data.get("language")),
            short_title=map_to_str(_data.get("shortTitle")),
            url=map_to_str(_data.get("url")),
            access_date=map_to_str(_data.get("accessDate")),
            archive=map_to_str(_data.get("archive")),
            archive_location=map_to_str(_data.get("archiveLocation")),
            library_catalog=map_to_str(_data.get("libraryCatalog")),
            call_number=map_to_str(_data.get("callNumber")),
            rights=map_to_str(_data.get("rights")),
            extra=map_to_str(_data.get("extra"))
        )
