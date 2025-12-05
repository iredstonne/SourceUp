from typing import TYPE_CHECKING, Iterable
if TYPE_CHECKING: from sourceup.client.zotero.ZoteroClientProtocol import ZoteroClientProtocol
if TYPE_CHECKING: from sourceup.collection.ZoteroCollection import ZoteroCollection
if TYPE_CHECKING: from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.client.zotero.ZoteroDataMapper import ZoteroDataMapper

class ZoteroDataRepository:
    def __init__(self, client: "ZoteroClientProtocol"):
        self._client = client

    def list_items(self) -> Iterable["ZoteroItem"]:
        _out = []
        for _item_raw in self._client.items():
            _item_mapped = ZoteroDataMapper.to_item(_item_raw)
            if _item_mapped:
                _out.append(_item_mapped)
        return _out

    def list_collections(self) -> Iterable["ZoteroCollection"]:
        _out = []
        for _collection_raw in self._client.collections():
            _collection_mapped = ZoteroDataMapper.to_collection(_collection_raw)
            if _collection_mapped:
                _out.append(_collection_mapped)
        return _out

    def list_collection_items(self, _collection: "ZoteroCollection") -> Iterable["ZoteroItem"]:
        _out = []
        for _collection_item_raw in self._client.collection_items(_collection.collection_key):
            _collection_item_mapped = ZoteroDataMapper.to_item(_collection_item_raw)
            if _collection_item_mapped:
                _out.append(_collection_item_mapped)
        return _out
