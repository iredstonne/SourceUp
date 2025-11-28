from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING: from sourceup.library.ZoteroLibrary import ZoteroLibrary
if TYPE_CHECKING: from sourceup.collection.ZoteroCollection import ZoteroCollection
if TYPE_CHECKING: from sourceup.item.ZoteroItem import ZoteroItem
from sourceup.client.zotero.PyZoteroClientProtocol import PyZoteroClientProtocol
from sourceup.client.zotero.ZoteroDataRepository import ZoteroDataRepository

def fetch_items(_library: "ZoteroLibrary") -> Iterable["ZoteroItem"]:
    _client = PyZoteroClientProtocol.from_library(_library)
    _repository = ZoteroDataRepository(_client)
    return _repository.list_items()

def fetch_collections(_library: "ZoteroLibrary") -> Iterable["ZoteroCollection"]:
    _client = PyZoteroClientProtocol.from_library(_library)
    _repository = ZoteroDataRepository(_client)
    return _repository.list_collections()

def fetch_collection_items(_library: "ZoteroLibrary", _collection: "ZoteroCollection") -> Iterable["ZoteroItem"]:
    _client = PyZoteroClientProtocol.from_library(_library)
    _repository = ZoteroDataRepository(_client)
    return _repository.list_collection_items(_collection)

def decipher_client_error(e: Exception):
    import traceback
    print("".join(traceback.format_exception(type(e), e, e.__traceback__)))

    from requests.exceptions import ConnectionError, ProxyError, SSLError, Timeout, ConnectTimeout, ReadTimeout, HTTPError

    if isinstance(e, (ConnectionError, ProxyError)):
        return (
            "Unable to reach Zotero.\n"
            "Please check your Internet connection or network configuration."
        )

    if isinstance(e, SSLError):
        return (
            "Unable to tie a secure connection with Zotero.\n"
            "Please check your system date and time settings or network configuration."
        )

    if isinstance(e, (Timeout, ConnectTimeout, ReadTimeout)):
        return (
            "Zotero took too long to respond.\n"
            "The operation timed out. Please try again in a moment."
        )

    return str(e)
