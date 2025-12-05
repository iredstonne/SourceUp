from pyzotero import zotero as _zlib
from typing import TYPE_CHECKING, Iterable, Any, Dict
if TYPE_CHECKING: from sourceup.library.ZoteroLibrary import ZoteroLibrary
from sourceup.client.zotero.ZoteroClientProtocol import ZoteroClientProtocol
from sourceup.client.zotero.PyZoteroClientConfig import PyZoteroClientConfig

class PyZoteroClientProtocol(ZoteroClientProtocol):
    def __init__(self, _z: _zlib.Zotero) -> None:
        self._z = _z

    def items(self) -> Iterable[Dict[str, Any]]:
        return self._z.everything(self._z.items())

    def collections(self) -> Iterable[Dict[str, Any]]:
        return self._z.everything(self._z.collections())

    def collection_items(self, _collection_key: str) -> Iterable[Dict[str, Any]]:
        return self._z.everything(self._z.collection_items(_collection_key))

    @classmethod
    def from_config(cls, _config: "PyZoteroClientConfig") -> "ZoteroClientProtocol":
        return cls(_config.create_client())

    @classmethod
    def from_library(cls, _library: "ZoteroLibrary") -> "ZoteroClientProtocol":
        return cls.from_config(PyZoteroClientConfig(_library))
