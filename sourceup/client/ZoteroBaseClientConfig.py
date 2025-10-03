from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, Generic
if TYPE_CHECKING: from sourceup.data.library.ZoteroLibrary import ZoteroLibrary

T = TypeVar("T")

@dataclass
class ZoteroBaseClientConfig(ABC, Generic[T]):
    library: ZoteroLibrary

    @abstractmethod
    def create_client(self) -> T: ...
