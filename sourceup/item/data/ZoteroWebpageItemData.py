from dataclasses import dataclass, fields
from typing import Optional, override, Dict, Any
from xml.etree.ElementTree import Element

from sourceup.item.ZoteroItemType import ZoteroItemType
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.casts import map_to_str

@dataclass(frozen=True, slots=True)
class ZoteroWebpageItemData(ZoteroBaseItemData):
    webpage_title: Optional[str] = None
    website_type: Optional[str] = None

    @override
    @classmethod
    def item_type(cls) -> ZoteroItemType:
        return ZoteroItemType.WEBPAGE

    @override
    @classmethod
    def map_from_data(cls, _data: Dict[str, Any]) -> "ZoteroWebpageItemData":
        _base_item_data = ZoteroBaseItemData.map_from_data(_data)
        return cls(
            **{_base_item_data_field.name: getattr(_base_item_data, _base_item_data_field.name)
               for _base_item_data_field in fields(ZoteroBaseItemData)},
            webpage_title=map_to_str(_data.get("webpageTitle")),
            website_type=map_to_str(_data.get("webpageType"))
        )

    @override
    def map_to_bibxml(self, _source_element: Element):
        ZoteroBaseItemData.map_to_bibxml(self, _source_element)
        pass
