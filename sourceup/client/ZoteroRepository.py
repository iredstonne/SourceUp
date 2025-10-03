from typing import TYPE_CHECKING, Iterable, List
if TYPE_CHECKING: from sourceup.client.ZoteroClientProtocol import ZoteroClientProtocol
if TYPE_CHECKING: from sourceup.data.collection.ZoteroCollection import ZoteroCollection
if TYPE_CHECKING: from sourceup.data.item.ZoteroItem import ZoteroItem
from sourceup.client.ZoteroMapper import ZoteroMapper


class ZoteroRepository:
    def __init__(self, client: "ZoteroClientProtocol"):
        self._client = client

    def list_items(self) -> Iterable["ZoteroItem"]:
        out: List["ZoteroItem"] = []
        for item_raw in self._client.items():
            item_mapped = ZoteroMapper.to_item(item_raw)
            if item_mapped:
                out.append(item_mapped)
        return out

    def list_collections(self) -> Iterable["ZoteroCollection"]:
        out: List["ZoteroCollection"] = []
        for collection_raw in self._client.collections():
            collection_mapped = ZoteroMapper.to_collection(collection_raw)
            if collection_mapped:
                out.append(collection_mapped)
        return out

    def list_collection_items(self, collection: "ZoteroCollection") -> Iterable["ZoteroItem"]:
        out: List["ZoteroItem"] = []
        for item_raw in self._client.collection_items(collection.key):
            item_mapped = ZoteroMapper.to_item(item_raw)
            if item_mapped:
                out.append(item_mapped)
        return out
