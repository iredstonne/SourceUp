import socket
import ssl
from typing import TYPE_CHECKING, Iterable
import httpx

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

    root_exception = e
    seen_root_exception_id = set()
    while True:
        root_exception_id = id(root_exception)
        if root_exception_id in seen_root_exception_id:
            break
        seen_root_exception_id.add(root_exception_id)
        next_root_exception = getattr(root_exception, "__cause__", None) or getattr(root_exception, "__context__", None)
        if not isinstance(next_root_exception, BaseException):
            break
        root_exception = next_root_exception

    if isinstance(root_exception, socket.gaierror):
        return (
            "The domain name could not be resolved for Zotero.\n"
            "Please check your network configuration and try again"
        )
    elif isinstance(root_exception, ssl.SSLError):
        return (
            "Unable to tie a secure connection with Zotero.\n"
            "Please check your system date/time and try again."
        )
    elif isinstance(root_exception, httpx.ProxyError):
        return (
            "Proxy error occurred while reaching Zotero.\n"
            "Please check your proxy configuration and try again."
        )
    elif isinstance(root_exception, ConnectionRefusedError):
        return (
            "Connection refused while reaching Zotero.\n"
            "Please check your network configuration and try again"
        )
    elif isinstance(root_exception, ConnectionResetError):
        return (
            "Connection interrupted while reaching Zotero.\n"
            "Please check your network stability and try again"
        )
    elif isinstance(root_exception, httpx.ConnectError):
        return (
            "Connection handshake failed while reaching Zotero.\n"
            "Please check your network configuration and try again."
        )
    elif isinstance(root_exception, httpx.TimeoutException):
        return (
            "Connection timed out while reaching Zotero\n"
            "Please try again in a moment."
        )

    return str(e)
