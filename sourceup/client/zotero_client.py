from typing import TYPE_CHECKING, Iterable
if TYPE_CHECKING: from sourceup.data.library.ZoteroLibrary import ZoteroLibrary
if TYPE_CHECKING: from sourceup.data.collection.ZoteroCollection import ZoteroCollection
if TYPE_CHECKING: from sourceup.data.item.ZoteroItem import ZoteroItem
from sourceup.client.PyZoteroClient import PyZoteroClient
from sourceup.client.ZoteroRepository import ZoteroRepository

def fetch_items(library: "ZoteroLibrary") -> Iterable["ZoteroItem"]:
    client = PyZoteroClient.from_library(library)
    repository = ZoteroRepository(client)
    return repository.list_items()

def fetch_collections(library: "ZoteroLibrary") -> Iterable["ZoteroCollection"]:
    client = PyZoteroClient.from_library(library)
    repository = ZoteroRepository(client)
    return repository.list_collections()

def fetch_collection_items(library: "ZoteroLibrary", collection: "ZoteroCollection") -> Iterable["ZoteroItem"]:
    client = PyZoteroClient.from_library(library)
    repository = ZoteroRepository(client)
    return repository.list_collection_items(collection)

