from typing import TYPE_CHECKING, Tuple, Type, Dict, Any
from sourceup.casts import map_to_str, normalize_str
if TYPE_CHECKING: from sourceup.data.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.data.item.ZoteroBookItemData import ZoteroBookItemData
from sourceup.data.item.ZoteroBookSectionItemData import ZoteroBookSectionItemData

class ZoteroItemDataFactory:
    _REGISTRY: Tuple[Type["ZoteroBaseItemData"], ...] = (
        ZoteroBookItemData,
        ZoteroBookSectionItemData
    )
    _CACHED_INDEX: Dict[str, Type[ZoteroBaseItemData]] = {}

    @classmethod
    def _key_from_item_data_cls(cls, item_data_cls: Type["ZoteroBaseItemData"]):
        return normalize_str(map_to_str(item_data_cls.item_type().lower()))

    @classmethod
    def _key_from_data(cls, data: Dict[str, Any]):
        return normalize_str(map_to_str(data.get("itemType").lower()))

    @classmethod
    def _build_cached_index(cls) -> Dict[str, Type[ZoteroBaseItemData]]:
        if cls._CACHED_INDEX:
            return cls._CACHED_INDEX
        index: Dict[str, Type[ZoteroBaseItemData]] = {}
        for item_data_cls in cls._REGISTRY:
            item_data_cls_key = cls._key_from_item_data_cls(item_data_cls)
            if item_data_cls_key in index:
                raise RuntimeError(f"Duplicate item data class key: {item_data_cls_key}")
            index[item_data_cls_key] = item_data_cls
        cls._CACHED_INDEX = index
        return index

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "ZoteroBaseItemData":
        index = cls._build_cached_index()
        cached_impl = index.get(cls._key_from_data(data))
        if cached_impl is None:
            raise ValueError(f"Unhandled item data: {data!r}")
        return cached_impl.map_from_data(data)
