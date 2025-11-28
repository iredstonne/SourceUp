from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Generic
if TYPE_CHECKING: from sourceup.library.ZoteroLibrary import ZoteroLibrary

TClient = TypeVar("TClient")

class BaseZoteroClientConfig(ABC, Generic[TClient]):
    _library: "ZoteroLibrary"

    def __init__(self, _library: "ZoteroLibrary"):
        self._library = _library

    @abstractmethod
    def create_client(self) -> TClient: ...
