from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from sourceup.casts import map_to_str
from sourceup.data.item.ZoteroBaseItemData import ZoteroBaseItemData


@dataclass(frozen=True, slots=True)
class ZoteroBookItemData(ZoteroBaseItemData):
    series: Optional[str] = None
    series_number: Optional[str] = None
    volume: Optional[str] = None
    number_of_volumes: Optional[str] = None
    edition: Optional[str] = None
    place: Optional[str] = None
    publisher: Optional[str] = None
    num_pages: Optional[str] = None
    isbn: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> str:
        return "book"

    @override
    @classmethod
    def map_from_data(cls, data: Dict[str, Any]) -> "ZoteroBookItemData":
        base_item_data = super().map_from_data(data)
        return cls(
            **{field.name: getattr(base_item_data, field.name) for field in fields(ZoteroBaseItemData)},
            series=map_to_str(data.get("series")),
            series_number=map_to_str(data.get("seriesNumber")),
            volume=map_to_str(data.get("volume")),
            number_of_volumes=map_to_str(data.get("numberOfVolumes")),
            edition=map_to_str(data.get("edition")),
            place=map_to_str(data.get("place")),
            publisher=map_to_str(data.get("publisher")),
            num_pages=map_to_str(data.get("numPages")),
            isbn=map_to_str(data.get("isbn"))
        )
