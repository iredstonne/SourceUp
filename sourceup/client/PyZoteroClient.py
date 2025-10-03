from pyzotero import zotero as _zlib
from typing import TYPE_CHECKING, Iterable, Any, Dict
if TYPE_CHECKING: from sourceup.client.PyZoteroClientConfig import PyZoteroClientConfig
if TYPE_CHECKING: from sourceup.data.library.ZoteroLibrary import ZoteroLibrary
from sourceup.client.ZoteroClientProtocol import ZoteroClientProtocol

class PyZoteroClient(ZoteroClientProtocol):
    def __init__(self, _z: _zlib.Zotero) -> None:
        self._z = _z

    def items(self) -> Iterable[Dict[str, Any]]:
        return self._z.everything(self._z.items())

    def collections(self) -> Iterable[Dict[str, Any]]:
        return self._z.everything(self._z.collections())

    def collection_items(self, collection_key: str) -> Iterable[Dict[str, Any]]:
        return self._z.everything(self._z.collection_items(collection_key))

    @classmethod
    def from_config(cls, config: "PyZoteroClientConfig") -> "PyZoteroClient":
        return cls(config.create_client())

    @classmethod
    def from_library(cls, library: "ZoteroLibrary") -> "PyZoteroClient":
        config = PyZoteroClientConfig(library)
        return cls(config.create_client())
