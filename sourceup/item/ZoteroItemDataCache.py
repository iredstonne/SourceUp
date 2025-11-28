from typing import Type, Dict, Optional
from sourceup.item.ZoteroBaseItemData import ZoteroBaseItemData
from sourceup.item.ZoteroItemDataRegistry import ZoteroItemDataRegistry
from sourceup.casts import normalize_str_case_insensitive

class ZoteroItemDataCache:
    _REGISTRY = ZoteroItemDataRegistry()
    _MEMO: Dict[str, Type["ZoteroBaseItemData"]]

    def __init__(self):
        self._MEMO = self._build_item_data_memo()

    def _build_item_data_memo(self) -> Dict[str, Type["ZoteroBaseItemData"]]:
        _item_data_memo = {}
        for item_data_cls in self._REGISTRY.ENTRIES:
            _item_type_key = normalize_str_case_insensitive(item_data_cls.item_type())
            if _item_type_key in _item_data_memo:
                raise ValueError(f"Duplicate Zotero item type '{_item_type_key}'  in {item_data_cls.__name__}")
            _item_data_memo[_item_type_key] = item_data_cls
        return _item_data_memo

    def resolve_item_data_from_memo(self, _item_type: str) -> Optional[Type["ZoteroBaseItemData"]]:
        return self._MEMO.get(normalize_str_case_insensitive(_item_type))
