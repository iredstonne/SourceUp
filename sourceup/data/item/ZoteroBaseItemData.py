from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any
from sourceup.casts import map_to_str
from sourceup.data.creator.ZoteroCreator import ZoteroCreator

@dataclass(frozen=True, slots=True)
class ZoteroBaseItemData(ABC):
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
    @abstractmethod
    def item_type(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroBaseItemData":
        return cls(
            title=map_to_str(data.get("title")),
            creators=tuple(ZoteroCreator.map_from_data(creator) for creator in data.get("creators") or ()),
            abstract_note=map_to_str(data.get("abstractNote")),
            date=map_to_str(data.get("date")),
            language=map_to_str(data.get("language")),
            short_title=map_to_str(data.get("shortTitle")),
            url=map_to_str(data.get("url")),
            access_date=map_to_str(data.get("accessDate")),
            archive=map_to_str(data.get("archive")),
            archive_location=map_to_str(data.get("archiveLocation")),
            library_catalog=map_to_str(data.get("libraryCatalog")),
            call_number=map_to_str(data.get("callNumber")),
            rights=map_to_str(data.get("rights")),
            extra=map_to_str(data.get("extra"))
        )
